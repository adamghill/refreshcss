import re

from refreshcss.css.rule import Rule
from refreshcss.html.site import Site

CSS_RULE_RE = re.compile(r"(([^{])+)\s*\{.*?\}", flags=re.DOTALL)
CSS_COMMENTS_RE = re.compile(r"/\*.*?\*/", flags=re.DOTALL)


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

        return new_css

    return css_text


def parse(css_text: str, site: Site) -> str:
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

    # TODO: Make Stylesheet which encapsulates all of this

    # Remove CSS comments for parsing purposes
    css_text = re.sub(CSS_COMMENTS_RE, "", css_text)

    # Take the internal selectors for media queries and make them regular selectors for parsing
    # This is required because CSS_RULE_RE isn't smart enough to handle media queries
    css_text = _pop_media_queries_out(css_text)

    for match in re.finditer(CSS_RULE_RE, css_text):
        css_rule = match.group(0).strip()
        rule = Rule(css_rule)

        # Remove any rule that is in the CSS, but is not used in the HTML for classes, elements, and ids
        for attr in ["classes", "elements", "ids"]:
            site_attr = getattr(site, attr)
            rule_attr = getattr(rule, attr)

            if rule_attr and site_attr and len(rule_attr & site_attr) == 0 or rule_attr and not site_attr:
                refreshed_css_text = refreshed_css_text.replace(str(rule), "")

    refreshed_css_text = _remove_empty_media_queries(refreshed_css_text)

    refreshed_css_text = refreshed_css_text.replace("\n\n", "\n")

    return refreshed_css_text
