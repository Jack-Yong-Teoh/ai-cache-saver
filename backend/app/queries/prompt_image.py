from typing import Optional, List
from sqlalchemy import BinaryExpression, ColumnOperators
from sqlalchemy.orm import Session
from app.models.databases.orm.prompt_image import PromptImage
from app.models.databases.queries.base import FilterModel, PaginateModel, SortModel
from app.queries.base import lazyload_data
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.databases.queries.prompt_image import (
    LazyloadPromptImageResultModel,
)


def get_prompt_image_filter_criterion(
    prompt_image_id: int = None,
    user_id: int = None,
    prompt_text: str = None,
    key_word: str = None,
    is_public: bool = None,
) -> List[BinaryExpression]:
    criterion = [
        (
            None
            if prompt_image_id is None
            else ColumnOperators.__eq__(PromptImage.id, prompt_image_id)
        ),
        (
            None
            if user_id is None
            else ColumnOperators.__eq__(PromptImage.user_id, user_id)
        ),
        (
            None
            if prompt_text is None
            else PromptImage.prompt_text.ilike(f"%{prompt_text}%")
        ),
        (None if key_word is None else PromptImage.key_word.ilike(f"%{key_word}%")),
        (
            None
            if is_public is None
            else ColumnOperators.__eq__(PromptImage.is_public, is_public)
        ),
    ]
    return [x for x in criterion if x is not None]


def get_prompt_images(
    db: Session,
    user_id: int = None,
    prompt_text: str = None,
    key_word: str = None,
    is_public: bool = None,
) -> List[PromptImage]:
    criterion = get_prompt_image_filter_criterion(
        user_id=user_id,
        prompt_text=prompt_text,
        key_word=key_word,
        is_public=is_public,
    )
    return db.query(PromptImage).filter(*criterion).all()


def get_prompt_image(
    db: Session,
    prompt_image_id: int = None,
    user_id: int = None,
    prompt_text: str = None,
    key_word: str = None,
    is_public: bool = None,
) -> Optional[PromptImage]:
    criterion = get_prompt_image_filter_criterion(
        prompt_image_id=prompt_image_id,
        user_id=user_id,
        prompt_text=prompt_text,
        key_word=key_word,
        is_public=is_public,
    )
    return db.query(PromptImage).filter(*criterion).one_or_none()


def save_prompt_image(
    db: Session, prompt_image: PromptImage, auto_commit: bool = True
) -> PromptImage:
    db.add(prompt_image)
    if auto_commit:
        db.commit()
        db.refresh(prompt_image)
    else:
        db.flush()
    return prompt_image


async def lazyload_prompt_images(
    async_db: AsyncSession,
    filters: list[FilterModel],
    pagination: PaginateModel,
    sort: SortModel,
    included_fields: list[str] = None,
    excluded_fields: list[str] = None,
    export: bool = False,
) -> LazyloadPromptImageResultModel:
    """
    Asynchronously loads prompt image data with filtering, sorting, and pagination.
    """
    select_query = select(
        PromptImage.id,
        PromptImage.prompt_text,
        PromptImage.image_url,
        PromptImage.created_date,
        PromptImage.modified_date,
    ).select_from(PromptImage)

    results = await lazyload_data(
        async_db=async_db,
        select_query=select_query,
        filters=filters,
        pagination=pagination,
        sort=sort,
        included_fields=included_fields,
        excluded_fields=excluded_fields,
        export=export,
    )

    return LazyloadPromptImageResultModel(**results.__dict__)
