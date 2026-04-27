from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.databases.orm.base import Base, AuditModel


class PromptImage(Base, AuditModel):
    __tablename__ = "prompt_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    prompt_text = Column(String, index=True, nullable=False)
    embedding = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    key_word = Column(String, index=True, nullable=True)

    user = relationship("User", back_populates="prompt_images")
