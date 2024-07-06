from dataclasses import dataclass

from refreshcss.css.at import At
from refreshcss.css.selector import Selector, SelectorType

SELECTOR_BREAKABLE_CHARACTER = {
    " ",
    ",",
    "\n",
    "{",
    "}",
    ":",
}
PORTION_BREAKING_CHARACTERS = {
    ".",
    "+",
    ">",
    "~",
    "||",
    "[",
}
ALL_BREAKING_CHARACTERS = PORTION_BREAKING_CHARACTERS | SELECTOR_BREAKABLE_CHARACTER


def _get_selectors_from_rule_portion(css_rule_portion) -> set[Selector]:
    """Get selectors from a portion of a rule."""

    selectors: set[Selector] = set()
    portion_length = len(css_rule_portion)
    portion_idx = 0
    starting_idx = 0
    inside_attribute_brackets = False

    while portion_length >= portion_idx:
        if portion_length == portion_idx:
            # It's the end of the string so add it as a selector and then bail
            part = css_rule_portion[starting_idx:portion_idx].strip()

            # Skip adding the end if it's a breakable character, e.g. +
            if part and part not in ALL_BREAKING_CHARACTERS:
                selectors.add(Selector(part))

            break

        c = css_rule_portion[portion_idx]

        if not inside_attribute_brackets and c in PORTION_BREAKING_CHARACTERS:
            part = css_rule_portion[starting_idx:portion_idx].strip()

            if part and part != ",":
                selectors.add(Selector(part))

                starting_idx = portion_idx
        elif c in (":",):
            # Start of a pseudo class so bail
            break
        elif c == "]":
            # End of an attribute so mark it
            inside_attribute_brackets = False

        if c == "[":
            # Start of an attribute so mark it
            inside_attribute_brackets = True

        portion_idx += 1

    return selectors


@dataclass(frozen=True, slots=True)
class Rule:
    """Domain object for a CSS rule which handles parsing the rule to retrieve all of its selectors.

    Note: Does not handle multiple rules or @media because those are removed prior to this
    object being used.
    """

    value: str

    def _get_selectors_of_type(self, selector_type: SelectorType) -> set[str]:
        """Helper method to get all selectors of a certain type.

        Args:
            selector_type: The selector type to filter selectors by.
        """

        _selectors = set()

        for selector in self.selectors:
            if selector.selector_type == selector_type:
                if selector.selector_type in (SelectorType.CLASS, SelectorType.ID):
                    _selectors.add(selector.value[1:])
                elif selector.selector_type == SelectorType.ATTRIBUTE:
                    attribute = selector.value[1:-1]

                    operators = ("*=", "$=", "^=", "|=", "~=", "=")

                    for operator in operators:
                        operator_idx = attribute.find(operator)

                        if operator_idx > -1:
                            attribute = attribute[:operator_idx].strip()
                            break

                    _selectors.add(attribute)
                else:
                    _selectors.add(selector.value)

        return _selectors

    @property
    def classes(self) -> set[str]:
        """All classes used in the rule.

        Note: These will be naked and not include a dot before them.
        """

        return self._get_selectors_of_type(SelectorType.CLASS)

    @property
    def ids(self) -> set[str]:
        """All ids used in the rule.

        Note: These will be naked and not include a hash before them.
        """

        return self._get_selectors_of_type(SelectorType.ID)

    @property
    def elements(self) -> set[str]:
        """All elements used in the rule."""

        return self._get_selectors_of_type(SelectorType.ELEMENT)

    @property
    def attributes(self) -> set[str]:
        """All attributes used in the rule."""

        return self._get_selectors_of_type(SelectorType.ATTRIBUTE)

    @property
    def selectors(self) -> set[Selector]:
        """All selectors used in the rule."""

        _selectors: set[Selector] = set()

        rule_length = len(self.value)
        char_idx = 0
        starting_idx = 0
        inside_at_rule = False

        while rule_length - 1 >= char_idx:
            c = self.value[char_idx]

            if c == "@":
                inside_at_rule = True
            elif inside_at_rule and c == ";":
                inside_at_rule = False
            elif not inside_at_rule and c in SELECTOR_BREAKABLE_CHARACTER:
                css_rule_portion = self.value[starting_idx:char_idx].strip()

                # Remove extraneous commas
                if css_rule_portion.startswith(","):
                    css_rule_portion = css_rule_portion[1:]

                if css_rule_portion.endswith(","):
                    css_rule_portion = css_rule_portion[:-1]

                if css_rule_portion:
                    _selectors |= _get_selectors_from_rule_portion(css_rule_portion)
                    starting_idx = char_idx

                if c == "{":
                    break

            char_idx += 1

        return _selectors

    @property
    def at(self) -> At | None:
        """At-rule for the rule."""

        rule_length = len(self.value)
        char_idx = 0
        starting_idx = 0
        bracket_count = 0

        while rule_length - 1 >= char_idx:
            c = self.value[char_idx]

            if c == ";":
                css_rule_portion = self.value[starting_idx : char_idx + 1].strip()

                return At(css_rule_portion)
            elif c == "{":
                bracket_count += 1
            elif c == "}":
                bracket_count -= 1

                if bracket_count == 0:
                    css_rule_portion = self.value[starting_idx : char_idx + 1].strip()

                    return At(css_rule_portion)

            char_idx += 1

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return self.value.__hash__()
