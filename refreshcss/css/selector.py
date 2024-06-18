from dataclasses import dataclass
from enum import Enum


class SelectorType(Enum):
    CLASS = 1
    ID = 2
    ELEMENT = 3


@dataclass(frozen=True)
class Selector:
    """Domain object for a CSS selector."""

    value: str

    @property
    def selector_type(self):
        if self.value.startswith("."):
            return SelectorType.CLASS
        elif self.value.startswith("#"):
            return SelectorType.ID
        else:
            return SelectorType.ELEMENT
