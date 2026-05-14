# Breeze-RP Backend

The backend for Breeze-RP, a minimalist, privacy-first roleplay application. Built with FastAPI, SQLAlchemy (async SQLite), and Rich logging.

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) (recommended)

## Local Development

### 1. Install Dependencies
```bash
uv sync
```

### 2. Configure Environment
Create a `.env` file in the `backend/` directory:
```env
IS_PROD=False
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
DATABASE_URL=sqlite+aiosqlite:///./data/breeze.db
```

### 3. Run the Server
```bash
uv run uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Swagger UI: `http://localhost:8000/docs`

## Testing

Run tests using pytest:
```bash
uv run pytest
```
Tests use an in-memory SQLite database and do not require external services.

## Deployment (Docker)

To run the entire stack (including the future frontend):
```bash
docker-compose up --build
```

For the backend alone:
```bash
docker build -t breeze-backend .
docker run -p 8000:8000 breeze-backend
```

## Architecture

- **Framework**: FastAPI (Async)
- **Database**: SQLite with `aiosqlite` and `sqlalchemy[asyncio]`
- **Logging**: `rich` with `IS_PROD` environment logic
- **Patterns**: Repository and Service patterns for clean domain logic
- **Testing**: TDD with vertical slices
