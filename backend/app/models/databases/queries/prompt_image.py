from typing import Optional, List
from datetime import datetime
from app.models.databases.queries.base import QueryResultModel, LazyLoadResult


class DetailedPromptImageQueryResultModel(QueryResultModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    prompt_text: Optional[str] = None
    embedding: Optional[str] = None
    image_url: Optional[str] = None
    is_public: Optional[bool] = None
    key_word: Optional[str] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


class LazyloadPromptImageQueryResultModel(QueryResultModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    prompt_text: Optional[str] = None
    image_url: Optional[str] = None
    is_public: Optional[bool] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


class LazyloadPromptImageResultModel(LazyLoadResult):
    data: List[LazyloadPromptImageQueryResultModel]
