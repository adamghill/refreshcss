set quiet
set dotenv-load
set export

# List commands
_default:
    just --list --unsorted --justfile {{justfile()}} --list-heading $'Available commands:\n'
  
# Install dependencies
bootstrap:
  uv sync

# Set up the project
setup:
  brew install pipx
  pipx ensurepath
  pipx install uv
  pipx install ruff

# Update the project
update:
  just lock
  uv sync --extra cli

# Lock the dependencies
lock:
  uv lock

# Lint the project
lint *ARGS='.':
  -ruff check {{ ARGS }}

# Check the types in the project
type *ARGS='':
  -uv run ty check {{ ARGS }}

# Benchmark the project
benchmark:
  -uv run pytest tests/benchmarks/ --benchmark-only --benchmark-compare

# Run the tests
test *ARGS='':
  -uv run pytest {{ ARGS }}

alias t := test

# Run coverage on the code
coverage:
  -uv run pytest --cov=refreshcss

# Run all the dev things
dev:
  just lint
  just type
  just coverage

# Build the package
build:
  uv build

# Build and publish the package to test PyPI and prod PyPI
publish:
  uv publish --publish-url https://test.pypi.org/legacy/
  uv publish
