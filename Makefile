.PHONY: help setup dev test migrate seed api fmt lint clean legacy legacy-setup openparliament-focus docs-audit docs-audit-strict lineage-auto features-stub verify-features ci-verify ten-pass-merge

# Default target
help:
	@echo "OpenPolicy Monorepo - Available Commands:"
	@echo ""
	@echo "Setup & Development:"
	@echo "  setup          - Install dependencies and setup environment"
	@echo "  dev            - Start development environment"
	@echo "  up             - Start services (alias for dev)"
	@echo "  down           - Stop all services"
	@echo "  logs           - Show service logs"
	@echo ""
	@echo "Legacy Code Management:"
	@echo "  legacy-setup   - Clone all repos to /legacy (reference only)"
	@echo "  openparliament-focus - Focus on OpenParliament integration"
	@echo ""
	@echo "Database:"
	@echo "  migrate        - Run database migrations"
	@echo "  migrate-create - Create new migration"
	@echo "  seed           - Seed database with sample data"
	@echo "  db-reset       - Reset database (DESTRUCTIVE)"
	@echo ""
	@echo "Testing:"
	@echo "  test           - Run all tests"
	@echo "  test-api       - Run API tests only"
	@echo "  test-etl       - Run ETL tests only"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  fmt            - Format code (Python + TypeScript)"
	@echo "  lint           - Lint code"
	@echo "  type-check     - Type check TypeScript code"
	@echo ""
	@echo "Utilities:"
	@echo "  clean          - Clean build artifacts and temporary files"
	@echo "  shell          - Open shell in running container"
	@echo "  psql           - Connect to PostgreSQL database"

# Setup environment
setup:
	@echo "Setting up OpenPolicy development environment..."
	@if command -v pnpm >/dev/null 2>&1; then \
		echo "Installing Node.js dependencies..."; \
		pnpm install --frozen-lockfile || true; \
	else \
		echo "pnpm not found, skipping Node.js setup"; \
	fi
	@if command -v uv >/dev/null 2>&1; then \
		echo "Installing Python dependencies..."; \
		uv pip compile -o services/api-gateway/requirements.txt pyproject.toml || true; \
	else \
		echo "uv not found, skipping Python setup"; \
	fi
	@echo "Setup complete!"

# Legacy code setup (reference only)
legacy-setup:
	@echo "Setting up legacy code reference structure..."
	@chmod +x scripts/clone_all.sh
	./scripts/clone_all.sh
	@echo ""
	@echo "Legacy code setup complete!"
	@echo "All repository code is now available in /legacy for reference"
	@echo "Focus on OpenParliament first: make openparliament-focus"

# OpenParliament focus mode
openparliament-focus:
	@echo "🎯 OpenParliament Focus Mode"
	@echo ""
	@echo "Current focus: Get OpenParliament fully working first"
	@echo ""
	@echo "Legacy code available in:"
	@echo "  - legacy/openparliament/ (Django app + data models)"
	@echo "  - legacy/scrapers-ca/ (provincial scrapers - review later)"
	@echo "  - legacy/civic-scraper/ (utilities - review later)"
	@echo ""
	@echo "Next steps:"
	@echo "1. Review legacy/openparliament/ structure"
	@echo "2. Extract data models and schema"
	@echo "3. Implement canonical database schema"
	@echo "4. Build OpenParliament ETL pipeline"
	@echo "5. Test API endpoints with real data"
	@echo ""
	@echo "Commands:"
	@echo "  make dev          - Start development environment"
	@echo "  make migrate      - Run database migrations"
	@echo "  make test         - Run tests"
	@echo "  make shell        - Open shell in API container"
	@echo "  make test-openparliament - Test OpenParliament integration"

# Development environment
dev up:
	@echo "Starting OpenPolicy development environment..."
	docker compose up -d --build
	@echo "Services started! API available at http://localhost:8080"
	@echo "Database available at localhost:5432"
	@echo "Use 'make logs' to view logs or 'make down' to stop"

quick-start:
	@echo "Quick starting OpenParliament system..."
	./scripts/quick_start.sh

down:
	@echo "Stopping OpenPolicy services..."
	docker compose down
	@echo "Services stopped"

logs:
	docker compose logs -f

# Database operations
migrate:
	@echo "Running database migrations..."
	docker compose exec api-gateway alembic upgrade head

migrate-create:
	@read -p "Enter migration name: " name; \
	docker compose exec api-gateway alembic revision --autogenerate -m "$$name"

seed:
	@echo "Seeding database with sample data..."
	docker compose --profile etl run --rm etl python -m etl.seed

db-reset:
	@echo "WARNING: This will destroy all data!"
	@read -p "Are you sure? Type 'yes' to confirm: " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker compose down -v; \
		docker compose up -d db; \
		echo "Database reset complete"; \
	else \
		echo "Database reset cancelled"; \
	fi

# Testing
test:
	@echo "Running all tests..."
	docker compose exec api-gateway pytest -v

test-api:
	@echo "Running API tests..."
	docker compose exec api-gateway pytest tests/api/ -v

test-etl:
	@echo "Running ETL tests..."
	docker compose --profile etl run --rm etl pytest tests/ -v

test-coverage:
	@echo "Running tests with coverage..."
	docker compose exec api-gateway pytest --cov=app --cov-report=html --cov-report=term

test-openparliament:
	@echo "Testing OpenParliament system integration..."
	./scripts/test_openparliament.sh

# Code quality
fmt:
	@echo "Formatting Python code..."
	docker compose exec api-gateway ruff check --fix . && black .
	@echo "Formatting TypeScript code..."
	@if command -v pnpm >/dev/null 2>&1; then pnpm run format; fi

lint:
	@echo "Linting Python code..."
	docker compose exec api-gateway ruff check . && black --check .
	@echo "Linting TypeScript code..."
	@if command -v pnpm >/dev/null 2>&1; then pnpm run lint; fi

type-check:
	@echo "Type checking TypeScript code..."
	@if command -v pnpm >/dev/null 2>&1; then pnpm run type-check; fi

# Utilities
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	@echo "Cleanup complete"

shell:
	@echo "Opening shell in API Gateway container..."
	docker compose exec api-gateway /bin/bash

psql:
	@echo "Connecting to PostgreSQL database..."
	docker compose exec db psql -U openpolicy -d openpolicy

# Health checks
health:
	@echo "Checking service health..."
	@curl -f http://localhost:8080/healthz || echo "API Gateway: DOWN"
	@docker compose exec db pg_isready -U openpolicy -d openpolicy || echo "Database: DOWN"

# Development shortcuts
restart-api:
	@echo "Restarting API Gateway..."
	docker compose restart api-gateway

rebuild:
	@echo "Rebuilding all services..."
	docker compose down
	docker compose up -d --build
<<<<<<< Current (Your changes)
=======

docs-audit:
	@bash scripts/docs_audit.sh

# Fails with non-zero exit if any checks fail (for CI use)
docs-audit-strict:
	@STRICT=1 bash scripts/docs_audit.sh

lineage-auto:
	@python3 scripts/generate_lineage.py

features-stub:
	@python3 scripts/ensure_feature_stubs.py

verify-features:
	@python3 scripts/verify_feature_checklist_ids.py

ten-pass-merge:
	@python3 scripts/ten_pass_merge.py

ci-verify: docs-audit-strict
	@echo "CI verify done."
>>>>>>> Incoming (Background Agent changes)
