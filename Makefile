.PHONY: venv install dev lint format test clean run run-sse example-client example-client-sse

# Variables
PYTHON = python3
VENV = .venv
BIN = $(VENV)/bin
PIP = $(BIN)/pip
UV = $(BIN)/uv
PORT ?= 8000
HOST ?= 0.0.0.0

# Main targets
venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -U pip setuptools uv

install: venv
	$(UV) pip install -e .

dev: venv
	$(UV) pip install -e ".[dev]"

lint:
	$(BIN)/black --check notion_mcp examples
	$(BIN)/isort --check notion_mcp examples
	$(BIN)/ruff check notion_mcp examples

format:
	$(BIN)/black notion_mcp examples
	$(BIN)/isort notion_mcp examples
	$(BIN)/ruff check --fix notion_mcp examples

test:
	$(BIN)/pytest -xvs tests

clean:
	rm -rf build/ dist/ *.egg-info/ .coverage .pytest_cache/ .ruff_cache/ __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run commands
run:
	$(BIN)/python -m notion_mcp.server --transport stdio

run-sse:
	$(BIN)/python -m notion_mcp.server --transport sse --host=$(HOST) --port=$(PORT)

example-client:
	$(BIN)/python examples/client_example.py

example-client-sse:
	$(BIN)/python examples/client_example.py --sse

help:
	@echo "Available commands:"
	@echo "  make venv              - Create a virtual environment"
	@echo "  make install           - Install the package"
	@echo "  make dev               - Install the package in development mode"
	@echo "  make lint              - Run linters"
	@echo "  make format            - Format code"
	@echo "  make test              - Run tests"
	@echo "  make clean             - Clean build artifacts"
	@echo "  make run               - Run the server with stdio transport"
	@echo "  make run-sse           - Run the server with SSE transport"
	@echo "  make example-client    - Run the example client using stdio transport"
	@echo "  make example-client-sse - Run the example client using SSE transport" 