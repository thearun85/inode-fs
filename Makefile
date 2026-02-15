.PHONY: lint fmt typecheck test all clean

# Run ruff lint check
lint:
	poetry run ruff check inode_fs/ tests/

# Run ruff format check
fmt:
	poetry run ruff format inode_fs/ tests/
	poetry run ruff check --fix inode_fs/ tests/

# Run mypy static type check
typecheck:
	poetry run mypy inode_fs/ tests/

# Run pytest
test:
	poetry run pytest -v -s

# Run all checks
all: lint fmt typecheck test

# Clean up the project files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
