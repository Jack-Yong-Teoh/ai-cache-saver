from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.databases.orm.user import User
from fastapi import Depends

from app.decorators.export import export_async
from app.models.databases.queries.prompt_image import LazyloadPromptImageResultModel
from app.models.pydantic_schemas.base import LazyloadRequestModel
from app.models.response_models.prompt_image import PromptImageResponseModel
from app.queries.prompt_image import (
    save_prompt_image,
    get_prompt_images,
    lazyload_prompt_images as query_lazyload_prompt_images,
)
from app.models.databases.orm.prompt_image import PromptImage
from app.utilities.postgresql import get_db, get_slave_db, get_async_slave_db
from app.utilities.logger import logger

from app.services.embedding import (
    generate_embedding,
    calculate_similarity,
    SIMILARITY_THRESHOLD,
)
from app.services.pollination import generate_image_content
from app.services.cloudinary import upload_image_to_cloud
from app.services.authentication import get_current_user


async def create_prompt_image(
    prompt_text: str,
    current_user: User = Depends(get_current_user),
    is_public: bool = True,
    db: Session = Depends(get_db),
    slave_db: Session = Depends(get_slave_db),
) -> PromptImageResponseModel:
    user_id = current_user.id
    """Handles logic for checking similarity, generating, and uploading images."""
    new_embedding = generate_embedding(prompt_text)

    existing_prompts = get_prompt_images(
        db=slave_db,
        is_public=True,
    )
    for entry in existing_prompts:
        similarity = calculate_similarity(new_embedding, entry.embedding)
        if similarity >= SIMILARITY_THRESHOLD:
            logger.debug(
                "Similarity found", extra={"similarity": similarity, "id": entry.id}
            )
            return entry

    logger.debug("No similarity found. Generating new image...")
    image_bytes = await generate_image_content(prompt_text)

    # Proper Cloudinary upload using the Python SDK
    cloud_url = upload_image_to_cloud(image_bytes)

    new_record = PromptImage(
        user_id=user_id,
        prompt_text=prompt_text,
        embedding=new_embedding,
        image_url=cloud_url,
        is_public=is_public,
        key_word=None,
    )

    return save_prompt_image(db=db, prompt_image=new_record)


@export_async
async def lazyload_prompt_images(
    payload: LazyloadRequestModel,
    async_slave_db: AsyncSession = Depends(get_async_slave_db),
    _: User = Depends(get_current_user),
) -> LazyloadPromptImageResultModel:
    """Asynchronously loads paginated and filtered prompt images."""
    logger.debug(
        "Lazyload Prompt Images Payload Received",
        extra={
            "payload": payload.model_dump(),
        },
    )
    return await query_lazyload_prompt_images(
        async_db=async_slave_db,
        filters=payload.filters,
        pagination=payload.pagination,
        sort=payload.sort,
        included_fields=payload.included_fields,
        excluded_fields=payload.excluded_fields,
        export=payload.export,
    )
