# ETL Service Makefile for OpenParliament.ca V2
# Following FUNDAMENTAL RULE: Uses legacy OpenParliament importers

.PHONY: help install collect-data test clean setup dev

help: ## Show this help message
	@echo "OpenParliament.ca V2 ETL Service"
	@echo "=================================="
	@echo ""
	@echo "Following FUNDAMENTAL RULE: Uses legacy OpenParliament importers"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies for legacy adapters
	pip install -r requirements.txt

collect-data: ## Collect parliamentary data using legacy OpenParliament importers
	@echo "🚀 Starting data collection using legacy OpenParliament importers..."
	@echo "📋 Following FUNDAMENTAL RULE: Never reinvent the wheel!"
	python collect_data.py

test: ## Run tests for legacy adapters
	pytest tests/ -v

clean: ## Clean up data and cache files
	rm -rf data/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete

setup: ## Set up development environment for legacy adapters
	@echo "🔧 Setting up ETL development environment..."
	@echo "📋 Following FUNDAMENTAL RULE: Using existing OpenParliament importers"
	python -m venv venv
	@echo "✅ Virtual environment created. Activate it with:"
	@echo "   source venv/bin/activate  # On Unix/macOS"
	@echo "   venv\\Scripts\\activate     # On Windows"
	@echo ""
	@echo "Then run: make install"

dev: ## Run in development mode with live reload
	@echo "🔄 Starting development mode..."
	@echo "📋 Using legacy OpenParliament importers"
	python -m watchdog.watchmedo auto-restart --patterns="*.py" --recursive -- python collect_data.py
