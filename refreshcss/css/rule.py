from dataclasses import dataclass

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
}
ALL_BREAKING_CHARACTERS = PORTION_BREAKING_CHARACTERS | SELECTOR_BREAKABLE_CHARACTER


@dataclass
class Rule:
    """Domain object for a CSS rule. Handles parsing the CSS to retrieve all of its selectors."""

    value: str

    def __init__(self, rule: str):
        self.value = rule
        self._selectors: set[Selector] = set()

    @staticmethod
    def _get_selectors_from_rule_portion(css_rule_portion) -> set[Selector]:
        """Get selectors from a portion of a rule."""

        selectors: set[Selector] = set()
        portion_length = len(css_rule_portion)
        portion_idx = 0
        starting_idx = 0

        while portion_length >= portion_idx:
            if portion_length == portion_idx:
                # It's the end of the string so add it as a selector and then bail
                part = css_rule_portion[starting_idx:portion_idx].strip()

                if part and part not in ALL_BREAKING_CHARACTERS:
                    # Skip adding the end if it's a breakable character, e.g. +
                    selectors.add(Selector(part))

                break

            c = css_rule_portion[portion_idx]

            if c in PORTION_BREAKING_CHARACTERS:
                part = css_rule_portion[starting_idx:portion_idx].strip()

                if part:
                    selectors.add(Selector(part))

                    starting_idx = portion_idx
            elif c in (":",):
                # It's the start of a pseudo class so bail
                # TODO: Can there be more than one pseduo class?
                break

            portion_idx += 1

        return selectors

    def _get_selectors(self) -> set[Selector]:
        """Get the selectors for a rule."""

        selectors: set[Selector] = set()

        rule_length = len(self.value)
        char_idx = 0
        bracket_count = 0
        starting_idx = 0

        while rule_length - 1 >= char_idx:
            c = self.value[char_idx]

            if c in SELECTOR_BREAKABLE_CHARACTER:
                if c == "{":
                    bracket_count += 1
                elif c == "}":
                    bracket_count -= 1
                    starting_idx = char_idx + 1

                if starting_idx > 0 and bracket_count > 0:
                    # Skip any characters that are _inside_ the brackets
                    char_idx += 1
                    continue

                css_rule_portion = self.value[starting_idx:char_idx].strip()

                if css_rule_portion:
                    selectors |= Rule._get_selectors_from_rule_portion(css_rule_portion)
                    starting_idx = char_idx

            char_idx += 1

        return selectors

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
    def selectors(self) -> set[Selector]:
        """All selectors used in the rule."""

        if not self._selectors:
            self._selectors = self._get_selectors()

        return self._selectors

    def __str__(self) -> str:
        return self.value