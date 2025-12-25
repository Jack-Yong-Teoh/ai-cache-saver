from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PromptImageResponseModel(BaseModel):
    id: Optional[int]
    prompt_text: Optional[str]
    image_url: Optional[str]
    created_date: Optional[datetime]
    modified_date: Optional[datetime]

    class Config:
        from_attributes = True
