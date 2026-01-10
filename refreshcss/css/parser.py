import tinycss2
from tinycss2.ast import AtRule, QualifiedRule

from refreshcss.html.site import Site


def _extract_selectors_from_tokens(tokens: list) -> list[tuple[set[str], set[str], set[str]]]:
    """
    Extract classes, ids, and elements from selector tokens, grouped by selector.

    Returns:
        List of (classes, ids, elements) tuples
    """
    selector_groups = []
    selector_text = tinycss2.serialize(tokens).strip()

    # Split by commas for multiple selectors
    for raw_selector in selector_text.split(","):
        selector = raw_selector.strip()
        classes = set()
        ids = set()
        elements = set()

        # Extract classes (anything after a dot)
        for part in selector.split():
            if "." in part:
                # Handle cases like "div.class" or ".class"
                class_parts = part.split(".")
                for raw_class_name in class_parts[1:]:  # Skip first part (element or empty)
                    # Clean up pseudo-classes, pseudo-elements, and attribute selectors
                    class_name = raw_class_name.split(":")[0].split("[")[0]
                    if class_name:
                        classes.add(class_name)

            if "#" in part:
                # Handle cases like "div#id" or "#id"
                id_parts = part.split("#")
                for raw_id_name in id_parts[1:]:
                    # Clean up pseudo-classes and attribute selectors
                    id_name = raw_id_name.split(":")[0].split("[")[0]
                    if id_name:
                        ids.add(id_name)

        # Extract element selectors (simple heuristic)
        # Look for bare words at the start of selectors or after combinators
        parts = selector.replace(">", " ").replace("+", " ").replace("~", " ").split()
        for part in parts:
            # Skip if it starts with . or # or is a pseudo-class/element
            if part and part[0] not in (".", "#", ":", "[", "*"):
                # Get just the element name (before any . or # or :)
                element = part.split(".")[0].split("#")[0].split(":")[0].split("[")[0]
                if element and element != "*":
                    elements.add(element)

        selector_groups.append((classes, ids, elements))

    return selector_groups


def _should_keep_rule(selector_groups: list[tuple[set[str], set[str], set[str]]], site: Site) -> bool:
    """
    Determine if a rule should be kept based on whether its selectors are used.

    A rule is kept if ANY of its comma-separated selectors are valid.
    A selector is valid if ALL of its specific parts (classes, ids) match.
    Element parts are only checked if there are no classes or ids in the selector.
    """
    for classes, ids, elements in selector_groups:
        is_selector_valid = True
        has_specific_matchers = False

        # Check classes
        if classes:
            has_specific_matchers = True
            if not site.classes or not classes.issubset(site.classes):
                is_selector_valid = False

        # Check ids
        if ids and is_selector_valid:
            has_specific_matchers = True
            if not site.ids or not ids.issubset(site.ids):
                is_selector_valid = False

        # Check elements
        if elements and is_selector_valid:
            # Only check elements if we don't have specific matchers (classes/ids)
            # This allows rules like ".table th" to be kept even if "th" is unused,
            # as long as ".table" is used.
            if not has_specific_matchers:
                # Special case: keep universal selector
                if "*" not in elements:
                    # Check elements against site.elements
                    # Use intersection (loose) to match legacy behavior where site.elements might be partial
                    if not site.elements or not (elements & site.elements):
                        is_selector_valid = False

        # If rule has no selectors we can identify, keep it
        if not classes and not ids and not elements:
            is_selector_valid = True

        if is_selector_valid:
            return True

    return False


def _parse_qualified_rule(rule: QualifiedRule, site: Site) -> str | None:
    """
    Parse a qualified rule (selector + declarations) and return CSS if it should be kept.

    Returns:
        CSS text if rule should be kept, None otherwise
    """
    selector_groups = _extract_selectors_from_tokens(rule.prelude)

    if _should_keep_rule(selector_groups, site):
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

    # Clean up excessive newlines
    while "\n\n\n" in result:
        result = result.replace("\n\n\n", "\n\n")

    return result
