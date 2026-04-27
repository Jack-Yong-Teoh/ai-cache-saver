# run the app
uvicorn app.main:app --reload --port 8888

# alembic
uv run alembic revision --autogenerate -m "Commit message"

# formatter
uv run black .

# activate the venv
source .venv/bin/activate