#* Install
.PHONY: install
install:
	uv sync

#* Clean
.PHONY: clean
clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .uv
	rm -rf dist
	rm src/kegstandcli/cdk.context.json
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +

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

#* Poetry (used for unit testing)
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

#* Test
.PHONY: test
test:
	uv run pytest -n auto -c pyproject.toml --cov-report=term --cov=src tests
