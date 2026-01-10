import re

import tinycss2
from tinycss2.ast import AtRule, QualifiedRule

from refreshcss.html.site import Site


def _rule_is_kept(tokens: list, site: Site) -> bool:
    """
    Determine if a rule should be kept by validating its selectors against the site.

    Optimized to run in a single pass over tokens without allocating intermediate
    sets or lists for every rule. Short-circuits as soon as a valid selector is found.
    """
    # State for the current selector being processed
    is_selector_valid = True
    has_specific_matchers = False
    current_elements = set()  # Lazily allocated only if needed? Set is needed for O(1) checks?
    # Actually intersection is fast. We typically have 0-1 elements.
    # Using a set is fine, it's small.

    # State flags for token parsing
    is_class = False
    expect_element = True  # True at start or after combinator

    for token in tokens:
        if token.type == "literal" and token.value == ",":
            # End of current selector. Check if it's valid.
            if is_selector_valid:
                # If we have specific matchers (classes/ids), elements are ignored unless none present
                # If no specific matchers, we check elements
                if has_specific_matchers:
                    return True  # Kept!

                # Check elements
                # Logic: if no specific matchers, check elements against site.elements
                keep_element = True
                if current_elements and "*" not in current_elements:
                    if not site.elements or not (current_elements & site.elements):
                        keep_element = False

                # Also if no selectors at all (empty?), we treat as valid/keep?
                # Logic from before: "If rule has no selectors we can identify, keep it"

                if keep_element:
                    return True

            # Reset for next selector
            is_selector_valid = True
            has_specific_matchers = False
            current_elements.clear()
            is_class = False
            expect_element = True
            continue

        # If already invalid, we can just skip tokens until comma?
        # But we need to parse correctly to find the comma.
        # Use a flag to "skip_until_comma"?
        # Tokenizer is flat, so we just continue iterating.

        if not is_selector_valid:
            continue

        if token.type == "whitespace":
            expect_element = True
            is_class = False
            continue

        if token.type == "literal":
            val = token.value
            if val == ".":
                is_class = True
                expect_element = False
            elif val in (">", "+", "~", "*"):
                is_class = False
                expect_element = True
            elif val == "*":
                current_elements.add("*")
                expect_element = False
            else:
                # Other syntax (prefixes, etc)
                is_class = False
                expect_element = False

        elif token.type == "ident":
            val = token.value
            if is_class:
                # Check class usage immediately
                has_specific_matchers = True
                if not site.classes or val not in site.classes:
                    is_selector_valid = False
                is_class = False

            elif expect_element:
                current_elements.add(val)
                expect_element = False
            else:
                pass

        elif token.type == "hash":
            # ID
            val = token.value
            has_specific_matchers = True
            if not site.ids or val not in site.ids:
                is_selector_valid = False
            expect_element = False

        else:
            is_class = False

    # Check the last selector (after loop finishes)
    if is_selector_valid:
        if has_specific_matchers:
            return True

        # Check elements
        if current_elements and "*" not in current_elements:
            if not site.elements or not (current_elements & site.elements):
                return False  # Drop

        # If no specific and valid elements (or empty), Keep.
        return True

    return False


def _parse_qualified_rule(rule: QualifiedRule, site: Site) -> str | None:
    """
    Parse a qualified rule (selector + declarations) and return CSS if it should be kept.

    Returns:
        CSS text if rule should be kept, None otherwise
    """
    if _rule_is_kept(rule.prelude, site):
        return tinycss2.serialize([rule])

    return None


def _parse_at_rule(rule: AtRule, site: Site) -> str | None:
    """
    Parse an at-rule (@media, @supports, @container, etc.) and return CSS if it should be kept.

    Returns:
        CSS text if rule should be kept, None otherwise
    """
    # Get the at-rule name (e.g., "media", "supports", "container")
    at_keyword = rule.at_keyword.lower()

    # Define at-rules that contain nested rules we should parse
    nested_at_rules = {"media", "supports", "container", "layer", "scope", "document"}

    # Handle nested at-rules (media queries, container queries, supports, etc.)
    if at_keyword in nested_at_rules and rule.content is not None:
        # Parse the content of the at-rule
        nested_rules = tinycss2.parse_rule_list(rule.content)
        kept_rules = []

        for nested_rule in nested_rules:
            if isinstance(nested_rule, QualifiedRule):
                nested_css = _parse_qualified_rule(nested_rule, site)
                if nested_css:
                    kept_rules.append(nested_css)
            elif isinstance(nested_rule, AtRule):
                nested_css = _parse_at_rule(nested_rule, site)
                if nested_css:
                    kept_rules.append(nested_css)

        # Only keep the at-rule if it has content
        if kept_rules:
            # Reconstruct the at-rule with filtered content
            at_rule_start = f"@{at_keyword} {tinycss2.serialize(rule.prelude).strip()} {{"
            at_rule_end = "}"
            return at_rule_start + "\n" + "\n".join(kept_rules) + "\n" + at_rule_end

    else:
        # Non-nested at-rules (e.g., @import, @charset, @font-face, @keyframes)
        # Keep these as they are (don't filter their content)
        return tinycss2.serialize([rule])

    return None


def parse(css_text: str, site: Site) -> str:
    """
    Parse CSS using tinycss2 and remove unused rules.

    This is a modern replacement for the regex-based parser that handles:
    - Modern CSS syntax (nested rules, container queries)
    - Complex selectors
    - Media queries
    - At-rules
    - Preserves comments

    Args:
        css_text: CSS to be parsed
        site: Site object with used classes, ids, and elements

    Returns:
        CSS text with only rules for selectors that are used
    """
    # Parse the CSS into rules (preserve comments)
    rules = tinycss2.parse_stylesheet(css_text, skip_comments=False)

    kept_css = []

    for rule in rules:
        if isinstance(rule, QualifiedRule):
            # Regular CSS rule (selector + declarations)
            css = _parse_qualified_rule(rule, site)
            if css:
                kept_css.append(css)

        elif isinstance(rule, AtRule):
            # At-rule (@media, @supports, @font-face, etc.)
            css = _parse_at_rule(rule, site)
            if css:
                kept_css.append(css)

        else:
            # Preserve comments and other tokens
            serialized = tinycss2.serialize([rule])
            if serialized.strip():  # Only add non-empty content
                kept_css.append(serialized)

    # Join all kept rules
    result = "\n".join(kept_css)

    # Clean up excessive newlines efficiently
    result = re.sub(r"\n{3,}", "\n\n", result)

    return result
