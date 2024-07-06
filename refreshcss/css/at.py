import re
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
            internal_rule = re.sub("@.*?{", "", self.value)
            last_bracket_idx = internal_rule.rindex("}")
            internal_rule = internal_rule[0:last_bracket_idx].strip()

            # Import here to avoid circular imports
            from refreshcss.css.rule import Rule

            return Rule(internal_rule)

        raise AttributeError("Regular at-rules do not have an internal rule")
