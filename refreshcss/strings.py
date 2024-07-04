from collections.abc import Generator


def remove_string_at(s: str, start_idx: int, end_idx: int) -> str:
    """Removes a substring from `s` from the start to the end index."""

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
