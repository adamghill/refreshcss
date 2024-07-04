set quiet
set dotenv-load
set export

# List commands
_default:
    just --list --unsorted --justfile {{justfile()}} --list-heading $'Available commands:\n'
  
# Install dependencies
bootstrap:
  poetry install

# Set up the project
setup:
  brew install pipx
  pipx ensurepath
  pipx install poetry
  pipx install ruff
  pipx install mypy

# Update the project
update:
  just lock
  poetry install

# Lock the dependencies
lock:
  poetry lock

# Lint the project
lint *ARGS='.':
  -ruff check {{ ARGS }}

# Check the types in the project
type *ARGS='.':
  -mypy {{ ARGS }}

# Benchmark the project
benchmark:
  -poetry run pytest tests/benchmarks/ --benchmark-only --benchmark-compare

# Run the tests
test *ARGS='':
  -poetry run pytest {{ ARGS }}

alias t := test

# Run coverage on the code
coverage:
  -poetry run pytest --cov=refreshcss

# Run all the dev things
dev:
  just lint
  just type
  just coverage

# Build the package
build:
  poetry build

# Build and publish the package to test PyPI and prod PyPI
publish:
  poetry publish --build -r test
  poetry publish
