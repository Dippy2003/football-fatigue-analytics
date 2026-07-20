.PHONY: setup dev backend-dev frontend-dev format lint typecheck test test-backend test-frontend build migrate docker-up docker-down ci verify-rights export-commit-log

setup:
	uv sync --project backend --all-groups
	npm --prefix frontend ci

dev:
	@echo "Run 'make backend-dev' and 'make frontend-dev' in separate terminals."

backend-dev:
	uv run --project backend uvicorn app.main:app --app-dir backend --reload

frontend-dev:
	npm --prefix frontend run dev

format:
	uv run --project backend ruff format backend scripts
	npm --prefix frontend run format

lint:
	uv run --project backend ruff format --check backend scripts
	uv run --project backend ruff check backend scripts
	npm --prefix frontend run format:check
	npm --prefix frontend run lint

typecheck:
	uv run --project backend mypy --config-file backend/pyproject.toml backend/app backend/tests scripts
	npm --prefix frontend run typecheck

test: test-backend test-frontend

test-backend:
	cd backend && uv run pytest

test-frontend:
	npm --prefix frontend test -- --run

build:
	npm --prefix frontend run build

migrate:
	uv run --project backend alembic -c backend/alembic.ini upgrade head

docker-up:
	docker compose up --build

docker-down:
	docker compose down

verify-rights:
	uv run --project backend python scripts/check_dataset_files.py

export-commit-log:
	uv run --project backend python scripts/export_commit_log.py

ci: lint typecheck test build verify-rights
	docker compose config --quiet
