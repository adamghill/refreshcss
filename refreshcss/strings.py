from typing import Generator


def remove_string_at(s, start_idx, end_idx) -> str:
    return s[0:start_idx] + s[end_idx:]


def finditer(needle: str, haystack: str) -> Generator[tuple[int, int], None, None]:
    """Yields a tuple of start and end indices for the `needle` in the `haystack`."""

    current = 0
    separator_len = len(needle)
    sections = haystack.split(needle)

    for section in sections[:-1]:  # skip trailing entry
        current += len(section)

        yield (current, current + separator_len)

        current += separator_len
