set dotenv-load
set positional-arguments
set quiet

default:
    just --list

# Lint the code
lint *args='.':
  ruff check $1

# Type-check the code
type *args='.':
  mypy $1

# Benchmark the code
benchmark:
  pytest tests/benchmarks/ --benchmark-only --benchmark-compare

# Run the tests
test *args='':
  poetry run pytest $1

# Run coverage on the code
cov:
  poetry run pytest --cov=refreshcss

# Run all the dev things
dev: lint type cov
  echo ""

# Build the package
build:
  poetry build

# Publish the package to PyPI
publish: build
  poetry publish --build -r test
  poetry publish
