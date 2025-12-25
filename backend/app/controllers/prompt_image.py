from sqlalchemy.orm import Session
from fastapi import Depends
from app.utilities.postgresql import get_db, get_slave_db
from app.queries.prompt_image import save_prompt_image, get_prompt_images
from app.models.databases.orm.prompt_image import PromptImage
from app.models.response_models.prompt_image import PromptImageResponseModel
from app.utilities.logger import logger

from app.services.embedding import (
    generate_embedding,
    calculate_similarity,
    SIMILARITY_THRESHOLD,
)
from app.services.pollination import generate_image_content
from app.services.cloudinary import upload_image_to_cloud


async def create_prompt_image(
    prompt_text: str,
    user_id: int,
    is_public: bool = True,
    db: Session = Depends(get_db),
    slave_db: Session = Depends(get_slave_db),
) -> PromptImageResponseModel:
    new_embedding = generate_embedding(prompt_text)

    existing_prompts = get_prompt_images(
        db=slave_db,
        is_public=True,
    )
    for entry in existing_prompts:
        similarity = calculate_similarity(new_embedding, entry.embedding)
        if similarity >= SIMILARITY_THRESHOLD:
            return entry

    # Generate image if no similar prompt found
    image_bytes = await generate_image_content(prompt_text)

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
