help:
  @just --list

install:
  @echo "🚀 Installing dependencies"
  @uv sync --all-extras --dev

install-pre-commit:
  @echo "🚀 Setting up the hooks"
  @uv run pre-commit install

check-project:
  @echo "🚀 Updating uv.lock"
  @uv lock
  @echo "🚀 Running the hooks against all files"
  @uv run pre-commit run --all-files

ruff:
  @echo "🚀 Linting the project with Ruff"
  @uv run ruff check .

ruff-show-violations:
  @echo "🚀 Linting the project with Ruff and show violations"
  @uv run ruff check --output-format="grouped" .

ruff-fix:
  @echo "🚀 Linting the project with Ruff and autofix violations (where possible)"
  @uv run ruff check --fix .

ruff-format:
  @echo "🚀 Formatting the code with Ruff"
  @uv run ruff format .

ruff-format-check:
  @echo "🚀 Listing files Ruff would reformat"
  @uv run ruff format --check .

lint-and-format: ruff-fix ruff-format

test:
  @echo "🚀 Testing code with pytest"
  @uv run pytest --verbose tests
