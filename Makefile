# Makefile for Sales Analytics project
# Unified command surface for installation, testing, documentation, and containerization.

SHELL := /bin/bash
PYTHON ?= $(shell which python3)
VENV ?= .venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip
VENV_PYTEST = $(VENV)/bin/pytest
VENV_SPHINX = $(VENV)/bin/sphinx-build

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help message
	@echo "========================================================================"
	@echo "Sales Analytics Project Automation"
	@echo "========================================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo "========================================================================"

.PHONY: venv
venv: ## Create virtual environment if it does not exist
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment in $(VENV)..."; \
		$(PYTHON) -m venv $(VENV); \
		$(VENV_PIP) install --upgrade pip; \
	fi

.PHONY: install
install: venv ## Install project in editable mode with development dependencies
	@echo "Installing project dependencies..."
	$(VENV_PIP) install -r requirements-dev.txt
	$(VENV_PIP) install -e .

.PHONY: test
test: ## Run unit and integration tests
	@if [ -f "$(VENV_PYTEST)" ]; then \
		$(VENV_PYTEST) -v; \
	else \
		python3 -m pytest -v; \
	fi

.PHONY: coverage
coverage: ## Run tests with code coverage report
	@if [ -f "$(VENV_PYTEST)" ]; then \
		$(VENV_PYTEST) --cov=sales --cov-report=term-missing --cov-report=html; \
	else \
		python3 -m pytest --cov=sales --cov-report=term-missing --cov-report=html; \
	fi

.PHONY: run
run: ## Run the CLI application with sample sales data
	@if [ -f "$(VENV_PYTHON)" ]; then \
		$(VENV_PYTHON) -m app.main -i data/sample_sales.csv; \
	else \
		python3 -m app.main -i data/sample_sales.csv; \
	fi

.PHONY: build
build: ## Build distributable sdist and wheel packages
	@echo "Building wheel and sdist packages..."
	@if [ -f "$(VENV_PYTHON)" ]; then \
		$(VENV_PYTHON) -m pip install --upgrade build; \
		$(VENV_PYTHON) -m build; \
	else \
		python3 -m build; \
	fi

.PHONY: docs
docs: ## Build Sphinx HTML documentation
	@echo "Building Sphinx documentation..."
	@if [ -f "$(VENV_SPHINX)" ]; then \
		$(VENV_SPHINX) -b html docs/source docs/build/html; \
	else \
		sphinx-build -b html docs/source docs/build/html; \
	fi

.PHONY: docker-build
docker-build: ## Build Docker container image
	docker build -t sales:0.1.0 .

.PHONY: docker-run
docker-run: ## Run application inside Docker container
	docker run --rm -v $$(pwd)/data:/app/data:ro sales:0.1.0 -i /app/data/sample_sales.csv

.PHONY: compose-up
compose-up: ## Run application using Docker Compose
	docker compose up --build

.PHONY: compose-down
compose-down: ## Stop and remove Docker Compose containers
	docker compose down

.PHONY: clean
clean: ## Remove temporary files, caches, and build artifacts
	@echo "Cleaning temporary files and build artifacts..."
	rm -rf build/ dist/ *.egg-info .eggs/
	rm -rf .pytest_cache .coverage htmlcov/
	rm -rf docs/build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
