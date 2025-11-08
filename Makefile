.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: update
update: ## Update the app packages
	uv lock --upgrade

.PHONY: add-dev-package
add-dev-package: ## Install a new dev package in the app. ex: make add-dev-package package=XXX
	uv add --dev $(package)

.PHONY: add-package
add-package: ## Install a new package in the app. ex: make add-package package=XXX
	uv add $(package)

.PHONY: remove-package
remove-package: ## Removes a package from the app. ex: make remove-package package=XXX
	uv remove $(package)

.PHONY: run
run: ## Run the app
	uv run fastapi run src/weather/delivery/api/main.py --reload

.PHONY: check-typing
check-typing:  ## Run a static analyzer over the code to find issues
	ty check .

.PHONY: check-lint
check-lint: ## Check the code style
	ruff check

.PHONY: lint
lint: ## Lint the code format
	ruff check --fix

.PHONY: check-format
check-format:  ## Check format python code
	ruff format --check

.PHONY: format
format:  ## Format python code
	ruff format

.PHONY: checks
checks: check-lint check-format check-typing  ## Run all checks

.PHONY: test
test: ## Run all the tests
	 PYTHONPATH=. pytest tests -ra -x --durations=5

.PHONY: pre-commit
pre-commit: checks test
