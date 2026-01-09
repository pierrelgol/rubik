# List available commands
default:
    @just --list

# Setup virtual environment and install dependencies
setup:
    uv venv
    uv pip install -e ".[dev]"

# Run the application with default input file
run *ARGS:
    uv run python -m src --input input.txt {{ARGS}}

# Run with custom arguments (no default input)
run-custom *ARGS:
    uv run python -m src {{ARGS}}

# Run the application in watch mode (auto-restart on file changes)
watch:
    uv run watchfiles 'uv run python -m src --input input.txt' src/

# Format code
fmt:
    uv run ruff format .
    uv run ruff check --fix .

# Check code style
check:
    uv run ruff check .

# Run tests
test:
    uv run pytest

# Clean up caches
clean:
    rm -rf .pytest_cache/ .ruff_cache/
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name '*.pyc' -delete

# Add a dependency
add PACKAGE:
    uv add {{PACKAGE}}
