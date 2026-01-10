from pathlib import Path

try:
    import charset_normalizer
except ImportError:
    charset_normalizer = None


def read_text(path: Path, encoding: str | None = None) -> str:
    """Open the file in text mode, read it, and close the file.

    If `encoding` is None and charset-normalizer is available, the encoding will be guessed.
    """

    if encoding or not charset_normalizer:
        return Path(path).read_text(encoding=encoding)

    best_match = charset_normalizer.from_path(path).best()

    if best_match:
        return str(best_match)
    else:
        raise ValueError("Unable to detect encoding.")
