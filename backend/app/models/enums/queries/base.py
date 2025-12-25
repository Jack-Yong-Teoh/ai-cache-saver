from typing import Union, Callable
from enum import Enum
from decimal import Decimal
from sqlalchemy import String, Text, Numeric
from sqlalchemy.sql.expression import ColumnOperators, func, cast
from sqlalchemy.sql.functions import coalesce

# pylint: disable-next=no-name-in-module
from sqlalchemy.sql.annotation import AnnotatedColumn
from sqlalchemy.sql.elements import Label


class FilterOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "gt"
    GREATER_THAN_EQUALS = "gte"
    LESSER_THAN = "lt"
    LESSER_THAN_EQUALS = "lte"
    BETWEEN = "between"
    NOT_BETWEEN = "not_between"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    CONTAINS_ALL = "contains_all"
    NOT_CONTAINS_ALL = "not_contains_all"
    CONTAINS_ANY = "contains_any"
    NOT_CONTAINS_ANY = "not_contains_any"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IS = "is"
    IS_NOT = "is_not"
    IN = "in"
    NOT_IN = "not_in"

    @staticmethod
    def equals(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        if isinstance(value, str):
            return ColumnOperators.__eq__(func.lower(field), func.lower(value))
        if isinstance(field.type, Numeric):
            return ColumnOperators.__eq__(field, Decimal(str(value)))
        return ColumnOperators.__eq__(field, value)

    @staticmethod
    def not_equals(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        return ColumnOperators.__invert__(FilterOperator.equals(field, value))

    @staticmethod
    def greater_than(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        if isinstance(field.type, Numeric):
            return ColumnOperators.__gt__(field, Decimal(str(value)))
        return ColumnOperators.__gt__(field, value)

    @staticmethod
    def greater_than_equals(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        if isinstance(field.type, Numeric):
            return ColumnOperators.__ge__(field, Decimal(str(value)))
        return ColumnOperators.__ge__(field, value)

    @staticmethod
    def lesser_than(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        if isinstance(field.type, Numeric):
            return ColumnOperators.__lt__(field, Decimal(str(value)))
        return ColumnOperators.__lt__(field, value)

    @staticmethod
    def lesser_than_equals(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        if isinstance(field.type, Numeric):
            return ColumnOperators.__le__(field, Decimal(str(value)))
        return ColumnOperators.__le__(field, value)

    @staticmethod
    def between(
        field: Union[AnnotatedColumn, Label],
        value: list,
    ):
        return ColumnOperators.between(field, value[0], value[1])

    @staticmethod
    def not_between(
        field: Union[AnnotatedColumn, Label],
        value: list,
    ):
        return ColumnOperators.__invert__(FilterOperator.between(field, value))

    @staticmethod
    def contains(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        _field = (
            field if isinstance(field.type, (String, Text)) else cast(field, String)
        )
        return ColumnOperators.contains(func.lower(_field), func.lower(value))

    @staticmethod
    def not_contains(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        return ColumnOperators.__invert__(FilterOperator.contains(field, value))

    @staticmethod
    def starts_with(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        _field = (
            field if isinstance(field.type, (String, Text)) else cast(field, String)
        )
        return ColumnOperators.startswith(func.lower(_field), func.lower(value))

    @staticmethod
    def ends_with(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        _field = (
            field if isinstance(field.type, (String, Text)) else cast(field, String)
        )
        return ColumnOperators.endswith(func.lower(_field), func.lower(value))

    @staticmethod
    def is_(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        if value is None:
            return ColumnOperators.__eq__(coalesce(cast(field, String), ""), "")
        return ColumnOperators.is_(field, value)

    @staticmethod
    def is_not(
        field: Union[AnnotatedColumn, Label],
        value: any,
    ):
        return ColumnOperators.__invert__(FilterOperator.is_(field, value))

    @staticmethod
    def in_(
        field: Union[AnnotatedColumn, Label],
        value: list,
    ):
        _field = func.lower(field) if isinstance(field.type, (String, Text)) else field
        return ColumnOperators.in_(
            _field,
            [
                func.lower(x) if isinstance(field.type, (String, Text)) else x
                for x in value
            ],
        )

    @staticmethod
    def not_in(
        field: Union[AnnotatedColumn, Label],
        value: list,
    ):
        return ColumnOperators.__invert__(FilterOperator.in_(field, value))

    @staticmethod
    def get_handler(operator: str) -> Callable:
        operators = {
            FilterOperator.EQUALS: FilterOperator.equals,
            FilterOperator.NOT_EQUALS: FilterOperator.not_equals,
            FilterOperator.GREATER_THAN: FilterOperator.greater_than,
            FilterOperator.GREATER_THAN_EQUALS: FilterOperator.greater_than_equals,
            FilterOperator.LESSER_THAN: FilterOperator.lesser_than,
            FilterOperator.LESSER_THAN_EQUALS: FilterOperator.lesser_than_equals,
            FilterOperator.BETWEEN: FilterOperator.between,
            FilterOperator.NOT_BETWEEN: FilterOperator.not_between,
            FilterOperator.CONTAINS: FilterOperator.contains,
            FilterOperator.NOT_CONTAINS: FilterOperator.not_contains,
            FilterOperator.STARTS_WITH: FilterOperator.starts_with,
            FilterOperator.ENDS_WITH: FilterOperator.ends_with,
            FilterOperator.IS: FilterOperator.is_,
            FilterOperator.IS_NOT: FilterOperator.is_not,
            FilterOperator.IN: FilterOperator.in_,
            FilterOperator.NOT_IN: FilterOperator.not_in,
        }
        return operators[operator]


class SortOrder(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"
