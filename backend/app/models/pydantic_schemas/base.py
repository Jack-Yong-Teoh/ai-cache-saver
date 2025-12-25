from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.databases.queries.base import (
    FilterModel,
    SortModel,
    PaginateModel,
)


class RequestModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class ResponseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class LazyloadRequestModel(RequestModel):
    filters: Optional[list[FilterModel]] = Field(
        default=[],
        examples=[
            [
                {
                    "field": "string",
                    "operator": "equals",
                    "value": "string",
                }
            ]
        ],
    )
    pagination: Optional[PaginateModel]
    sort: Optional[SortModel] = Field(default=None)
    included_fields: Optional[list[str]] = Field(
        default=[],
    )
    excluded_fields: Optional[list[str]] = Field(
        default=[],
    )
    export: Optional[bool] = Field(default=False)


class EnumResponseModel(BaseModel):
    value: str
    label: str
    model_config = ConfigDict(
        extra="allow",
    )
