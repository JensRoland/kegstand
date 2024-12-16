#* Install
.PHONY: install
install:
	uv sync

#* Format
.PHONY: lint-fix
lint-fix:
	uv run ruff format
	uv run ruff check --fix

#* Lint
.PHONY: lint-check
lint-check:
	uv run ruff check

.PHONY: mypy
mypy:
	uv run mypy --config-file pyproject.toml src tests

.PHONY: lint
lint: lint-check mypy

#* Test
.PHONY: test
test:
	uv run pytest -c pyproject.toml --cov-report=term --cov=src tests
