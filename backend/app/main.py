from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import prompt_image
from app.routes import authentication

app = FastAPI(title="AI Cache Saver")

# Basic CORS to prevent browser blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Only the route you care about
app.include_router(
    prompt_image.router,
    prefix="/prompt-image",
    tags=["prompt-image"],
)

app.include_router(
    authentication.router,
    prefix="/auth",
    tags=["auth"],
)


@app.get("/health")
async def health():
    return {"status": "running"}
