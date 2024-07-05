from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class At:
    """Domain object for a CSS at-rule.

    https://developer.mozilla.org/en-US/docs/Web/CSS/At-rule
    """

    value: str

    @property
    def is_nested(self) -> bool:
        return "{" in self.value

    @property
    def internal_rule(self) -> str:
        if self.is_nested:
            raise NotImplementedError()

        raise AttributeError("Regular at-rules do not have an internal rule")
