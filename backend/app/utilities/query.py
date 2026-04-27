from typing import Union

# pylint: disable-next=no-name-in-module
from sqlalchemy.sql.annotation import AnnotatedColumn
from sqlalchemy.sql.elements import Label
from sqlalchemy.sql.selectable import Select


def extract_tables_from_select(select_query: Select) -> dict:
    tables = {}

    def extract_tables_from_join(join) -> dict:
        join_tables = {}
        for side in [join.left, join.right]:
            # It's a column, get the table
            if hasattr(side, "table"):
                join_tables[side.table.name] = side.table

            # It's a table
            elif hasattr(side, "name"):
                join_tables[side.name] = side

            # It's another join, recursive
            elif hasattr(side, "left") and hasattr(side, "right"):
                join_tables.update(extract_tables_from_join(side))

        return join_tables

    for from_clause in select_query.get_final_froms():
        # It's a join
        if hasattr(from_clause, "left") and hasattr(from_clause, "right"):
            tables.update(extract_tables_from_join(from_clause))
    return tables


def has_aggregation_function(field: Union[AnnotatedColumn, Label]):
    if isinstance(field, Label):
        return has_aggregation_function(field.element)

    if getattr(field, "name", "").lower() in [
        "count",
        "min",
        "max",
        "avg",
        "sum",
        "string_agg",
        "array_agg",
    ]:
        return True

    if hasattr(field, "clauses"):
        return any(has_aggregation_function(arg) for arg in field.clauses)

    if hasattr(field, "left"):
        return has_aggregation_function(field.left)

    return False
