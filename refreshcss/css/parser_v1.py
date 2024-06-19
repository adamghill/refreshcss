import re

CSS_RULE_RE = re.compile(r"(([^{])+)\s*\{.*?\}", flags=re.DOTALL)
CSS_COMMENTS_RE = re.compile(r"/\*.*?\*/", flags=re.DOTALL)


def _handle_css_rule_part(css_rule_part: str, css_classes: set, ids: set) -> bool:
    if css_rule_part:
        if css_rule_part.startswith("."):
            css_classes.add(css_rule_part[1:])
        elif css_rule_part.startswith("#"):
            ids.add(css_rule_part[1:])

        return True

    return False


def _get_css_classes_and_ids(css_rule: str) -> tuple[set, set]:
    """
    Get the CSS classes and IDs referenced
    """

    css_classes: set[str] = set()
    ids: set[str] = set()

    bracket_count = 0

    for rule_idx, r in enumerate(css_rule):
        if r in ("+", ">", ":", "||", "~", " ", ",", "\n", "{"):
            if r == "{":
                bracket_count += 1
            elif r == "}":
                bracket_count -= 1

            css_rule_portion = css_rule[:rule_idx]

            if css_rule_portion:
                starting_idx = 0

                for portion_idx, p in enumerate(css_rule_portion):
                    if p in (".", "#"):
                        css_rule_part = css_rule_portion[starting_idx:portion_idx]

                        if _handle_css_rule_part(css_rule_part, css_classes, ids):
                            starting_idx = portion_idx
                    elif portion_idx == len(css_rule_portion) - 1:
                        # Handle the last portion
                        css_rule_part = css_rule_portion[starting_idx : portion_idx + 1]

                        _handle_css_rule_part(css_rule_part, css_classes, ids)

            if bracket_count == 0:
                (_css_classes, _ids) = _get_css_classes_and_ids(css_rule[rule_idx + 1 :])
                css_classes |= _css_classes
                ids |= _ids

            return (css_classes, ids)

    return (css_classes, ids)


def _remove_empty_media_queries(css_text: str) -> str:
    return re.sub(r"@media[^{]+\{[\n\s]*\}", "", css_text)


def _pop_media_queries_out(css_text: str) -> str:
    previous_ending_idx = 0
    ending_idx = -1
    new_css = ""

    for media_match in re.finditer(r"@media", css_text):
        starting_idx = media_match.start()
        starting_bracket_count = 0
        has_hit_an_ending_bracket = False
        starting_rule_idx = -1
        ending_idx = 0

        for idx, c in enumerate(css_text):
            if idx < starting_idx:
                continue

            if c == "{":
                starting_bracket_count += 1

                if starting_bracket_count == 1 and starting_rule_idx == -1:
                    starting_rule_idx = idx + 1
            elif c == "}":
                starting_bracket_count -= 1
                has_hit_an_ending_bracket = True

                if starting_bracket_count == 0 and has_hit_an_ending_bracket:
                    ending_idx = idx
                    break

        new_css += css_text[previous_ending_idx:starting_idx] + css_text[starting_rule_idx:ending_idx]

        previous_ending_idx = ending_idx + 1

    if previous_ending_idx > 0 and ending_idx > -1:
        # Add any additional css that wasn't matched
        new_css += css_text[ending_idx + 1 :]

        # print("new_css", new_css)

        return new_css

    return css_text


def parse(css_text: str, html_classes: set[str], html_ids: set[str]) -> str:
    """Parse CSS and remove any class rules that are not in the set of CSS classes.

    Note: This is not an actual parser and is pretty unsophisticated, but it kind of works ok.

    Args:
        css_text: CSS to be parsed.
        html_classes: Set of currently used CSS classes in the HTML.
        html_ids: Set of currently used ids in the HTML.

    Returns:
        CSS text which only contains rules for the classes which are currently being used.
    """

    # Make a copy of the CSS for cleaning up later
    refreshed_css_text = css_text

    # Remove CSS comments for parsing purposes
    css_text = re.sub(CSS_COMMENTS_RE, "", css_text)

    # Take the internal selectors for media queries and make them regular selectors for parsing
    css_text = _pop_media_queries_out(css_text)

    for match in re.finditer(CSS_RULE_RE, css_text):
        css_classes: set[str] = set()
        css_rule = match.group(0).strip()

        # TODO: Handle html_ids
        (css_classes, ids) = _get_css_classes_and_ids(css_rule)

        if css_classes and html_classes and len(css_classes & html_classes) == 0 or css_classes and not html_classes:
            refreshed_css_text = refreshed_css_text.replace(css_rule, "")

    # TODO: Handle html_ids
    # if ids and html_ids and len(ids & html_ids) == 0:
    #     fresh_css_text = fresh_css_text.replace(css_rule, "")

    refreshed_css_text = _remove_empty_media_queries(refreshed_css_text)

    refreshed_css_text = refreshed_css_text.replace("\n\n", "\n")

    return refreshed_css_text
