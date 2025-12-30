import httpx
from urllib.parse import quote
import os

# Your API Key
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")


async def generate_image_content(prompt: str) -> bytes:
    """Generates image via Pollinations AI using an API key."""
    encoded_prompt = quote(prompt)

    # Use the API endpoint for authenticated requests
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    # Standard parameters for high quality
    params = {
        "width": 1024,
        "height": 1024,
        "seed": 42,
        "model": "flux",
        "nologo": "true",
    }

    headers = {"Authorization": f"Bearer {POLLINATIONS_API_KEY}", "Accept": "image/*"}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, params=params, headers=headers, timeout=90.0)

        if response.status_code == 200:
            if "image" in response.headers.get("Content-Type", ""):
                return response.content
            raise Exception(
                f"Expected image, got {response.headers.get('Content-Type')}"
            )

        # Log the error detail if available
        error_detail = response.text
        raise Exception(
            f"Pollinations AI Error ({response.status_code}): {error_detail}"
        )
