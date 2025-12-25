from typing import Optional, Any
from sqlalchemy.engine.row import Row
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.models.enums.queries.base import (
    FilterOperator,
    SortOrder,
)
from app.utilities.datetime import str2date


class FilterModel(BaseModel):
    field: str
    operator: FilterOperator
    value: Optional[Any]

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
    )

    @model_validator(mode="after")
    # pylint: disable-next=no-self-argument
    def root_validator_handler(cls, model_instance: "FilterModel"):
        field = model_instance.field
        operator = model_instance.operator

        # All fields filtering logic
        if field == "*" and operator not in [
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.CONTAINS,
            FilterOperator.NOT_CONTAINS,
            FilterOperator.STARTS_WITH,
            FilterOperator.ENDS_WITH,
        ]:
            raise ValueError("Unsupported operator for all fields")

        # Return the model instance after validation
        return model_instance

    @field_validator("value")
    # pylint: disable-next=too-many-branches
    def validate_value(cls, v, values):
        operator = values.data.get("operator")

        # Null/Empty filtering
        if v is None:
            if operator not in [
                FilterOperator.IS,
                FilterOperator.IS_NOT,
            ]:
                raise ValueError("Unsupported operator for null value")
            return v

        # Date filtering
        if isinstance(v, str):
            dt = str2date(v, raise_error=False)
            if dt is not None:
                if operator not in [
                    FilterOperator.GREATER_THAN,
                    FilterOperator.GREATER_THAN_EQUALS,
                    FilterOperator.LESSER_THAN,
                    FilterOperator.LESSER_THAN_EQUALS,
                ]:
                    raise ValueError("Unsupported operator for datetime value")

                if (
                    operator
                    in [
                        FilterOperator.GREATER_THAN,
                        FilterOperator.LESSER_THAN_EQUALS,
                    ]
                    and dt.strftime("%H:%M:%S.%f") == "00:00:00.000000"
                ):
                    dt = dt.replace(
                        hour=23,
                        minute=59,
                        second=59,
                        microsecond=999999,
                    )
                return dt

        # Date range filtering
        if isinstance(v, list) and len(v) == 2 and all(isinstance(x, str) for x in v):
            dt_from = str2date(v[0], raise_error=False)
            dt_to = str2date(v[1], raise_error=False)
            if dt_from is not None:
                if dt_to is not None and operator not in [
                    FilterOperator.BETWEEN,
                    FilterOperator.NOT_BETWEEN,
                ]:
                    raise ValueError("Unsupported operator for ranged datetime value")

                if (
                    dt_from.strftime("%H:%M:%S.%f") == "00:00:00.000000"
                    and dt_to.strftime("%H:%M:%S.%f") == "00:00:00.000000"
                ):
                    dt_to = dt_to.replace(
                        hour=23,
                        minute=59,
                        second=59,
                        microsecond=999999,
                    )
                return [dt_from, dt_to]

        # String filtering
        if isinstance(v, str) and operator not in [
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.CONTAINS,
            FilterOperator.NOT_CONTAINS,
            FilterOperator.STARTS_WITH,
            FilterOperator.ENDS_WITH,
        ]:
            raise ValueError("Unsupported operator for string value")

        # Numeric filtering
        if (
            isinstance(v, (int, float))
            and not isinstance(v, bool)
            and operator
            not in [
                FilterOperator.EQUALS,
                FilterOperator.NOT_EQUALS,
                FilterOperator.GREATER_THAN,
                FilterOperator.GREATER_THAN_EQUALS,
                FilterOperator.LESSER_THAN,
                FilterOperator.LESSER_THAN_EQUALS,
            ]
        ):
            raise ValueError("Unsupported operator for numeric value")

        # Boolean filtering
        if isinstance(v, bool) and operator not in [
            FilterOperator.IS,
            FilterOperator.IS_NOT,
        ]:
            raise ValueError("Unsupported operator for boolean value")

        # List filtering
        if isinstance(v, list) and operator not in [
            FilterOperator.IN,
            FilterOperator.NOT_IN,
            FilterOperator.CONTAINS_ALL,
            FilterOperator.NOT_CONTAINS_ALL,
            FilterOperator.CONTAINS_ANY,
            FilterOperator.NOT_CONTAINS_ANY,
        ]:
            raise ValueError("Unsupported operator for list value")
        return v


class PaginateModel(BaseModel):
    limit: int = Field(
        ge=0,
        json_schema_extra={"example": 10},
    )
    page: Optional[int] = Field(default=1, ge=0)

    model_config = ConfigDict(extra="forbid")


class SortModel(BaseModel):
    order_by: Optional[str] = Field(json_schema_extra={"example": "id"})

    sort_order: Optional[SortOrder] = Field(
        json_schema_extra={"example": SortOrder.DESCENDING}
    )

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
    )

    @field_validator("sort_order")
    def validate_sort_order(cls, v, values):
        order_by = values.data.get("order_by")
        if v is not None and order_by is None:
            raise ValueError("`order_by` is required")
        return v


class QueryResultModel(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class LazyLoadResult(BaseModel):
    columns: list[str]
    data: list[Row]
    count: int

    model_config = ConfigDict(arbitrary_types_allowed=True)
