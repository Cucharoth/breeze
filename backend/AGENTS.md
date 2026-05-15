# Agent Development Guidelines: Backend

This document outlines the established development practices, architecture, and conventions for the Breeze-RP backend. Any AI agent modifying this codebase MUST adhere to these rules.

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite (via SQLAlchemy + async `aiosqlite`)
- **Validation**: Pydantic v2
- **Language**: Python 3.12+

## Architecture & Data Flow
- **Validation**: Pydantic v2. All API inputs/outputs must be validated via Pydantic schemas (defined in `app/schemas/`). Use `ConfigDict(from_attributes=True)` for ORM compatibility.
- **Domain-Driven Design**: The application logic strictly flows from:
  `Routers (endpoints)` -> `Services (business logic)` -> `Repositories (DB access)`.
- **Repository Pattern**: All database access goes through `app/repositories/`. New repositories must inherit from `BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]` for standard CRUD operations.
- **Async Patterns**: Everything is fully async. Use async route handlers, async DB operations (`AsyncSession`), and FastAPI `BackgroundTasks` for non-blocking operations like knowledge extraction.
- **LLM Architecture**:
  - We use a **Protocol-based Provider** model (`app/services/llm/interface.py`).
  - Do NOT inherit from Abstract Base Classes (ABCs). Implement the `LLMProvider` protocol (e.g., `OllamaProvider`, `GeminiProvider`).
  - **The Game Master**: All LLM operations are orchestrated centrally by `LLMService` in `app/services/llm_service.py`. Endpoints must depend on `get_llm_service` and pass it to the business logic.

## Logging & Terminal Noise (CRITICAL)
- **Library**: Custom `logger` in `app.core.logger`.
- **Rule**: Do NOT use standard `print()` statements. Use the centralized `logger` instance.
- **Layered Logging**:
  - **API Layer (Routers)**: Use `logger.info()` to log major user actions (e.g., "Igniting reality with premise..."). Keep it clean and sparse.
  - **Service Layer**: Use `logger.debug()` to trace business logic flow, DB persistence, and generation phases.
  - **Provider Layer**: Use `logger.debug()` to log raw API requests/responses.
- **Database Silence**: SQLAlchemy `echo` is explicitly set to `False` in `app/core/database.py`. The `logger.py` suppresses library logs (`uvicorn`, `sqlalchemy.engine`) to `WARNING`. Do NOT turn these back on to `INFO` unless actively debugging a severe crash. The terminal must remain clean.

## Database & Migrations
- **Alembic**: All model changes (`app/models/`) require an Alembic migration.
- Models should inherit from `Base` in `app/core/database.py`.
- Always use `Mapped` and `mapped_column` (SQLAlchemy 2.0 style) for model declarations.

## Game Loop Specifics
- **Streaming**: The Game Master (LLM) responses are streamed using Server-Sent Events (SSE) for optimal user experience. Use `StreamingResponse` from FastAPI.
- **Directives & Actors**: Adhere to the terms in `CONTEXT.md` (e.g., `Actor`, `Directive`). Directives are strictly bound to a specific `Branch`, not a global `Story`.
