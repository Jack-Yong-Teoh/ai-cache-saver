from typing import Optional
from datetime import datetime


class PromptImageResultModel:
    id: Optional[int]
    user_id: Optional[int]
    prompt_text: Optional[str]
    embedding: Optional[str]
    image_url: Optional[str]
    is_public: Optional[bool]
    key_word: Optional[str]
    created_date: Optional[datetime]
    modified_date: Optional[datetime]
