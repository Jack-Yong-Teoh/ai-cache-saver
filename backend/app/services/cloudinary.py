import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_image_to_cloud(image_bytes: bytes, folder: str = "prompts") -> str:
    """Uploads bytes directly to Cloudinary."""
    # The Python SDK can take raw bytes directly
    upload_result = cloudinary.uploader.upload(
        image_bytes, folder=folder, resource_type="image"
    )
    return upload_result.get("secure_url")
