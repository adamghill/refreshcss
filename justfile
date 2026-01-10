import? 'adamghill.justfile'
import? '../dotfiles/just/justfile'

src := "src/django_new"

# List commands
_default:
    just --list --unsorted --justfile {{ justfile() }} --list-heading $'Available commands:\n'

# Grab default `adamghill.justfile` from GitHub
fetch:
  curl https://raw.githubusercontent.com/adamghill/dotfiles/master/just/justfile > adamghill.justfile

# Benchmark the project
benchmark:
  -uv run pytest tests/benchmarks/ --benchmark-only --benchmark-compare
