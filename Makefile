now := $(shell date -u '+%Y%m%d-%H%M')

#* Install
.PHONY: install
install:
	uv sync

#* Clean
.PHONY: purgecache
purgecache:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +

#* Clean
.PHONY: clean
clean: purgecache
	rm -rf .temp
	rm -rf .uv
	rm -rf build
	rm src/kegstandcli/cdk.context.json

#* Format
.PHONY: lint-fix
lint-fix:
	uv run ruff format
	uv run ruff check --fix

#* Lint
.PHONY: lint-check
lint-check:
	uv run ruff check

.PHONY: lint-types
lint-types:
	uv run mypy --config-file pyproject.toml src tests

.PHONY: lint
lint: lint-check lint-types

#* CDK CLI
.PHONY: cdk-download
cdk-download:
	@echo "Installing AWS CDK..."
	@npm install -g aws-cdk

#* Poetry (used for unit testing)
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

#* Test
.PHONY: test
test:
	uv run pytest -c pyproject.toml --cov-report=term --cov=src tests

# Splitting the e2e into multiple steps to make it easier to debug:
#* E2E Test - Create
.PHONY: e2e-create-project
e2e-create-project:
	@echo "Running E2E tests..."
	@rm -rf .temp
	@mkdir -p .temp
	@echo "Creating a new project in kegstand-test-$(now)..."
	@cd .temp && uv run keg new --data-file ../tests/test_data/e2e-uv.yaml kegstand-test-$(now)

#* E2E Test - Build
.PHONY: e2e-build
e2e-build:
	@echo "Building..."
	@uv run keg --config .temp/kegstand-test-$(now)/pyproject.toml build

#* E2E Test - Deploy
.PHONY: e2e-deploy
e2e-deploy:
	@echo "Deploying..."
	@uv run keg --verbose --config .temp/kegstand-test-$(now)/pyproject.toml deploy --skip-build

#* E2E Test - Test
.PHONY: e2e-test
e2e-test:
	@echo "Testing..."
	@(uv run keg --config .temp/kegstand-test-$(now)/pyproject.toml test-api-endpoint hello || (EXIT_CODE=$$?; \
		echo "Tearing down after test failure..." && \
		cd .temp/kegstand-test-$(now) && uv run keg teardown && \
		exit $$EXIT_CODE))

#* E2E Test - Teardown
.PHONY: e2e-teardown
e2e-teardown:
	@echo "Tearing down..."
	@cd .temp/kegstand-test-$(now) && uv run keg teardown
	@echo "Done"

#* E2E Test - All
.PHONY: e2e
e2e: | e2e-create-project e2e-build e2e-deploy e2e-test e2e-teardown
