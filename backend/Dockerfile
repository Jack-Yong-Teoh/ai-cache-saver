# Use Python 3.11 slim image
FROM python:3.11-slim-bookworm

# 1. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# 2. Copy dependency files first
COPY pyproject.toml uv.lock ./

# 3. Install dependencies
# --frozen: Use the exact versions in uv.lock
# --no-install-project: Only install libraries, not your own app (since code isn't copied yet)
RUN uv sync --frozen --no-install-project

# 4. Copy the rest of the application
COPY . .

# 5. Install the project itself (if your app is a package)
RUN uv sync --frozen

# 6. IMPORTANT: Add the virtual environment to the PATH
# This ensures 'uvicorn' and 'python' run from the .venv automatically
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8888

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888"]