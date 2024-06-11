help:
  @just --list

install:
  @echo "🚀 Installing dependencies"
  @poetry install --with dev

install-pre-commit:
  @echo "🚀 Setting up the hooks"
  @poetry run pre-commit install

check-project:
  @echo "🚀 Checking consistency between poetry.lock and pyproject.toml"
  @poetry check --lock
  @echo "🚀 Running the hooks against all files"
  @poetry run pre-commit run --all-files

ruff:
  @echo "🚀 Linting the project with Ruff"
  @poetry run ruff check .

ruff-show-violations:
  @echo "🚀 Linting the project with Ruff and show violations"
  @poetry run ruff check --output-format="grouped" .

ruff-fix:
  @echo "🚀 Linting the project with Ruff and autofix violations (where possible)"
  @poetry run ruff check --fix .

ruff-format:
  @echo "🚀 Formatting the code with Ruff"
  @poetry run ruff format .

ruff-format-check:
  @echo "🚀 Listing files Ruff would reformat"
  @poetry run ruff format --check .

lint-and-format: ruff-fix ruff-format

test:
  @echo "🚀 Testing code with pytest"
  @poetry run pytest --verbose tests
