.PHONY: lint fmt typecheck test all clean

# Run ruff lint check
lint:
	poetry run ruff check inode_fs/ tests/

# Run ruff format check
fmt:
	peotry run ruff format inode_fs/ tests/
	peotry run ruff check --fix inode_fs/ tests/

# Run mypy static type check
typecheck:
	poetry run mypy typecheck inode_fs/ tests/

# Run pytest
test:
	poetry run pytest -v

# Run all checks
all: lint fmt typecheck test

# Clean up the project files
clean:
	find . -type d -name __pycache__ rm -rf {} +
	find . -type d -name .mypy_cache rm -rf {} +
	find . -type d -name .pytest_cache rm -rf {} +
