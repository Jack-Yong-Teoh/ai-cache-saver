from typing import Union, Type
from functools import reduce
from sqlalchemy import (
    func,
    asc,
    desc,
    union_all,
    or_,
    and_,
    literal_column,
    select,
    ColumnOperators,
    Select,
    CompoundSelect,
    BinaryExpression,
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import Row
from app.models.databases.orm.base import Base
from app.models.databases.queries.base import (
    FilterModel,
    SortModel,
    PaginateModel,
)
from app.models.enums.queries.base import FilterOperator, SortOrder

from app.models.databases.queries.base import LazyLoadResult
from app.models.exceptions import NotFoundException, LogicException
from app.utilities.query import (
    has_aggregation_function,
)
from app.utilities.config import CONFIG


def get_orm_filter_criterion(
    orm_model: Type[Base],  # type: ignore
    filters: list[FilterModel],
) -> list[BinaryExpression]:
    filter_criterion = []
    for filter_model in filters:
        operator_handler = FilterOperator.get_handler(filter_model.operator)
        column = orm_model.__table__.columns.get(filter_model.field)
        filter_criterion.append(
            operator_handler(column, filter_model.value),
        )
    return filter_criterion


def handle_filters(
    select_query: Select,
    filters: list[FilterModel] = None,
) -> Select:
    filters = [] if filters is None else filters
    if not filters:
        return select_query

    filter_criterion = []
    having_criterion = []

    for filter_model in filters:
        if filter_model.field == "*":
            # Generate filtering criteria for all columns with OR condition
            operator_handler = FilterOperator.get_handler(filter_model.operator)
            having_criterion.append(
                or_(
                    *[
                        operator_handler(v, filter_model.value)
                        for _, v in select_query.selected_columns.items()
                        if has_aggregation_function(v)
                    ]
                )
            )
            filter_criterion.append(
                or_(
                    *[
                        operator_handler(v, filter_model.value)
                        for _, v in select_query.selected_columns.items()
                        if not has_aggregation_function(v)
                    ]
                )
            )
        else:
            # Find column from select query
            select_column = next(
                iter(
                    [
                        v
                        for k, v in select_query.selected_columns.items()
                        if k == filter_model.field
                    ]
                ),
                None,
            )
            if select_column is None:
                raise LogicException(
                    f"Filtering is not supported for field `{filter_model.field}`"
                )

            # Generate filtering criteria
            operator_handler = FilterOperator.get_handler(filter_model.operator)
            if has_aggregation_function(select_column):
                having_criterion.append(
                    operator_handler(select_column, filter_model.value)
                )
            else:
                filter_criterion.append(
                    operator_handler(select_column, filter_model.value)
                )

    select_query = select_query.filter(*filter_criterion)
    if having_criterion:
        select_query = select_query.having(and_(*having_criterion))
    return select_query


def handle_sort(
    select_query: Select,
    sort: SortModel = None,
) -> Select:
    if sort is not None and sort.order_by is not None:
        # Find column from select query
        select_column = next(
            iter(
                [
                    v
                    for k, v in select_query.selected_columns.items()
                    if k == sort.order_by
                ]
            ),
            None,
        )
        if select_column is None:
            raise LogicException(
                f"Sorting is not supported for field `{sort.order_by}`"
            )

        # Generate sorting criteria
        sort_order = desc if sort.sort_order == SortOrder.DESCENDING else asc
        select_query = select_query.order_by(*[sort_order(select_column)])
    return select_query


def handle_pagination(
    select_query: Select,
    pagination: PaginateModel = None,
    for_union: bool = False,
) -> Select:
    if pagination.limit < 1:
        return select_query
    if pagination.page == 0:
        return select_query.limit(literal_column(f"{pagination.limit}"))
    if pagination:
        limit = pagination.limit * pagination.page if for_union else pagination.limit
        offset = 0 if for_union else pagination.limit * (pagination.page - 1)
        return select_query.limit(literal_column(f"{limit}")).offset(
            literal_column(f"{offset}")
        )
    return select_query


def handle_included_columns(
    select_query: Select,
    included_fields: list[str] = None,
) -> Select:
    included_fields = included_fields if included_fields else ["*"]
    if "*" not in included_fields:
        select_query = select_query.with_only_columns(
            *[x for x in select_query.selected_columns if x.name in included_fields]
        )
    return select_query


def handle_excluded_columns(
    select_query: Select,
    excluded_fields: list[str] = None,
) -> Select:
    if excluded_fields:
        select_query = select_query.with_only_columns(
            *[x for x in select_query.selected_columns if x.name not in excluded_fields]
        )
    return select_query


def handle_pre_lazyloading(
    select_query: Select,
    filters: list[FilterModel] = None,
    pagination: PaginateModel = None,
    sort: SortModel = None,
    included_fields: list[str] = None,
    excluded_fields: list[str] = None,
    for_union: bool = False,
    export: bool = False,
) -> Select:
    select_query = handle_filters(
        select_query=select_query,
        filters=filters,
    )
    select_query = handle_sort(
        select_query=select_query,
        sort=sort,
    )
    # No pagination for data export
    if pagination and not export:
        select_query = handle_pagination(
            select_query=select_query,
            pagination=pagination,
            for_union=for_union,
        )
    select_query = handle_included_columns(
        select_query=select_query,
        included_fields=included_fields,
    )
    select_query = handle_excluded_columns(
        select_query=select_query,
        excluded_fields=excluded_fields,
    )
    return select_query


def generate_count_query(
    select_query: Select,
) -> Select:
    # pylint:disable-next=protected-access
    group_by_clauses = select_query._group_by_clauses
    count_query = (
        # pylint: disable-next=not-callable
        select_query.with_only_columns(func.count(literal_column("1")).label("count"))
        .order_by(None)
        .limit(None)
        .offset(None)
    )

    # pylint:disable-next=protected-access
    if select_query._having_criteria:
        count_query = select(
            # pylint:disable-next=not-callable
            func.count(literal_column("1")).label("count")
        ).select_from(count_query)
        return count_query

    if group_by_clauses:
        count_query = (
            select_query.with_only_columns(
                # pylint:disable-next=not-callable
                func.count(func.distinct(*group_by_clauses)).label("count")
            )
            .order_by(None)
            .limit(None)
            .offset(None)
            .group_by(None)
        )
        return count_query

    return count_query


async def optimized_lazyload_union_data(
    async_db: AsyncSession,
    select_query_mappings: dict[
        str, Union[Select, CompoundSelect, list[Select], list[CompoundSelect]]
    ],
    select_query_filter_model: FilterModel,
    filters: list[FilterModel] = None,
    sort: SortModel = None,
    pagination: PaginateModel = None,
    included_fields: list[str] = None,
    excluded_fields: list[str] = None,
    export: bool = False,
) -> LazyLoadResult:
    select_queries = []

    # Include only necessary queries
    if select_query_filter_model:
        mappings = {
            k: {"query": v, "include": False} for k, v in select_query_mappings.items()
        }
        filter_operator = select_query_filter_model.operator
        filter_values = (
            select_query_filter_model.value
            if isinstance(select_query_filter_model.value, list)
            else [select_query_filter_model.value]
        )
        for k, v in mappings.items():
            if (
                filter_operator in [FilterOperator.IN, FilterOperator.EQUALS]
                and k in filter_values
            ) or (
                filter_operator in [FilterOperator.NOT_IN, FilterOperator.NOT_EQUALS]
                and k not in filter_values
            ):
                v["include"] = True

        select_queries = [
            y
            for k, v in mappings.items()
            for y in (v["query"] if isinstance(v["query"], list) else [v["query"]])
            if v["include"]
        ]

    # Include all queries
    if not select_queries:
        select_queries = [
            y
            for x in select_query_mappings.values()
            for y in (x if isinstance(x, list) else [x])
        ]

    if len(select_queries) == 1:
        return await lazyload_data(
            async_db=async_db,
            select_query=select_queries[0],
            filters=filters,
            sort=sort,
            pagination=pagination,
            included_fields=included_fields,
            excluded_fields=excluded_fields,
            export=export,
        )

    return await lazyload_union_data(
        async_db=async_db,
        select_queries=select_queries,
        filters=filters,
        sort=sort,
        pagination=pagination,
        included_fields=included_fields,
        excluded_fields=excluded_fields,
        export=export,
    )


async def lazyload_union_data(
    async_db: AsyncSession,
    select_queries: list[Select],
    filters: list[FilterModel] = None,
    sort: SortModel = None,
    pagination: PaginateModel = None,
    included_fields: list[str] = None,
    excluded_fields: list[str] = None,
    export: bool = False,
) -> LazyLoadResult:
    # Validate number of SELECT statements
    if len(select_queries) <= 1:
        raise ValueError("More than 1 SELECT query is expected")

    # Validate SELECT statement fields
    select_queries_columns = [
        [x.name for x in select_query.selected_columns]
        for select_query in select_queries
    ]
    if len({tuple(x) for x in select_queries_columns}) > 1:
        raise ValueError(
            "Columns on SELECT queries are expected to have the same name and order"
        )

    # Build SELECT & COUNT statements
    select_queries = [
        handle_pre_lazyloading(
            select_query=select_query,
            filters=filters,
            sort=sort,
            pagination=pagination,
            included_fields=included_fields,
            excluded_fields=excluded_fields,
            for_union=True,
            export=export,
        )
        for select_query in select_queries
    ]
    count_queries = [
        generate_count_query(select_query).label("count")
        for select_query in select_queries
    ]

    select_query = union_all(*select_queries)
    count_query = select(reduce(ColumnOperators.__add__, count_queries).label("count"))

    return await lazyload_data(
        async_db=async_db,
        select_query=select_query,
        count_query=count_query,
        sort=sort,
        pagination=pagination,
        export=export,
    )


async def lazyload_data(
    async_db: AsyncSession,
    select_query: Union[Select, CompoundSelect],
    count_query: Union[Select, CompoundSelect] = None,
    filters: list[FilterModel] = None,
    pagination: PaginateModel = None,
    sort: SortModel = None,
    included_fields: list[str] = None,
    excluded_fields: list[str] = None,
    export: bool = False,
) -> LazyLoadResult:
    # Handle pre-processing for lazy-loading (filters, sorting, etc.)
    select_query = handle_pre_lazyloading(
        select_query=select_query,
        filters=filters,
        pagination=pagination,
        sort=sort,
        included_fields=included_fields,
        excluded_fields=excluded_fields,
        export=export,
    )
    # Generate COUNT statement from SELECT statement if not provided
    if count_query is None:
        count_query = generate_count_query(select_query)

    # Apply SELECT statement filtering to COUNT statement
    elif isinstance(select_query, Select):
        count_query = count_query.filter(select_query.whereclause)

    select_result = await async_db.execute(select_query)
    count_result = await async_db.execute(count_query)

    count = (
        count_result.scalar()
        if not pagination
        else (
            count_result.scalar()
            if pagination.page > 0 or pagination.limit < 1
            else min(count_result.scalar(), pagination.limit)
        )
    )

    if export and count > int(CONFIG.OTHER.DATA_EXPORT_LIMIT):
        raise LogicException(
            "DATA_EXPORT_EXCEED_LIMIT",
            extra={"count": count},
        )

    return LazyLoadResult(
        columns=[x.name for x in select_query.selected_columns],
        data=select_result.all(),
        count=count,
    )


def get_detailed_row(
    db: Session,
    select_query: Select,
    target: str,
    included_fields: list[str] = None,
    optional: bool = False,
) -> Row:
    select_query = handle_included_columns(
        select_query=select_query,
        included_fields=included_fields,
    )

    db_row = db.execute(select_query).one_or_none()
    if db_row is None and not optional:
        raise NotFoundException(f"{target}_NOT_FOUND")
    return db_row
