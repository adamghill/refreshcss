import pytest
from refreshcss.css.parser import parse

from tests.utils import assert_css


def test_parse():
    expected = """
body { color: 'blue'; }

.test-1 { color: 'red'; }
"""

    css_text = """
body { color: 'blue'; }

.test-1 { color: 'red'; }

.test-2 { color: 'green'; }
"""

    actual = parse(css_text, {"test-1"}, set())

    assert_css(expected, actual)


def test_parse_media_query():
    expected = """
@media screen and (max-width: 1408px) {
  .is-shadowless {
    visibility: hidden !important;
  }
}
"""

    css_text = """
@media screen and (min-width: 1408px) {
  .is-visibility-hidden-fullhd,
  .is-invisible-fullhd {
    visibility: hidden !important;
  }
}

@media screen and (max-width: 1408px) {
  .is-shadowless {
    visibility: hidden !important;
  }
}
"""

    actual = parse(css_text, {"is-shadowless"}, set())

    assert_css(expected, actual)


def test_parse_longer():
    expected = """
body {
  color: var(--bulma-body-color);
  font-size: var(--bulma-body-font-size);
  font-weight: var(--bulma-body-weight);
  line-height: var(--bulma-body-line-height);
}

.is-shadowless {
  box-shadow: none !important;
}
"""

    css_text = """
body {
  color: var(--bulma-body-color);
  font-size: var(--bulma-body-font-size);
  font-weight: var(--bulma-body-weight);
  line-height: var(--bulma-body-line-height);
}

@media screen and (min-width: 1408px) {
  .is-visibility-hidden-fullhd,
  .is-invisible-fullhd{
    visibility: hidden !important;
  }
}
.is-radiusless {
  border-radius: 0 !important;
}

.is-shadowless {
  box-shadow: none !important;
}

.is-clickable {
  cursor: pointer !important;
  pointer-events: all !important;
}
"""

    actual = parse(css_text, {"is-shadowless"}, set())

    assert_css(expected, actual)


def test_parse_additional():
    expected = """
.header {
    font-weight: bold;
}"""

    css_text = """
.container,
.last-commit {
    margin-left: 0px;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_multiple():
    expected = """
.header.last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    css_text = """
.container {
    margin-left: 0px;
}
.header.last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_descendant():
    expected = """
.header .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    css_text = """
.container {
    margin-left: 0px;
}
.header .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_pseudo():
    expected = """
.header:empty {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    css_text = """
.container {
    margin-left: 0px;
}
.header:empty {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_sibling():
    expected = """
.header+.last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    css_text = """
.container {
    margin-left: 0px;
}
.header + .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_child():
    expected = """
.header>.last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    css_text = """
.container {
    margin-left: 0px;
}
.header > .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_precede():
    expected = """
.header~.last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    css_text = """
.container {
    margin-left: 0px;
}
.header ~ .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_column():
    expected = """
.header||.last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    css_text = """
.container {
    margin-left: 0px;
}
.header || .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_1():
    expected = """
.header {
    font-weight: bold;
}"""

    css_text = """
.icon + a {
    padding-left: 28px;
}
.header {
    font-weight: bold;
}"""

    actual = parse(css_text, {"header"}, set())

    assert_css(expected, actual)


def test_parse_2():
    """It would be nice to remove all of the selectors that are not being used."""

    expected = """
.skeleton-block:not(:last-child), .media:not(:last-child), .level:not(:last-child), .fixed-grid:not(:last-child), .grid:not(:last-child), .tabs:not(:last-child), .pagination:not(:last-child), .message:not(:last-child), .card:not(:last-child), .breadcrumb:not(:last-child), .field:not(:last-child), .file:not(:last-child), .title:not(:last-child),
.subtitle:not(:last-child), .tags:not(:last-child), .table:not(:last-child), .table-container:not(:last-child), .progress:not(:last-child), .notification:not(:last-child), .content:not(:last-child), .buttons:not(:last-child), .box:not(:last-child), .block:not(:last-child) {
  margin-bottom: var(--bulma-block-spacing);
}"""

    css_text = """
.skeleton-block:not(:last-child), .media:not(:last-child), .level:not(:last-child), .fixed-grid:not(:last-child), .grid:not(:last-child), .tabs:not(:last-child), .pagination:not(:last-child), .message:not(:last-child), .card:not(:last-child), .breadcrumb:not(:last-child), .field:not(:last-child), .file:not(:last-child), .title:not(:last-child),
.subtitle:not(:last-child), .tags:not(:last-child), .table:not(:last-child), .table-container:not(:last-child), .progress:not(:last-child), .notification:not(:last-child), .content:not(:last-child), .buttons:not(:last-child), .box:not(:last-child), .block:not(:last-child) {
  margin-bottom: var(--bulma-block-spacing);
}"""

    actual = parse(css_text, {"media"}, set())

    assert_css(expected, actual)


def test_parse_bulma_subset():
    expected = ""

    css_text = """
@media screen and (min-width: 769px)and (max-width: 1023px){.is-invisible-tablet-only{visibility:hidden !important}}@media screen and (max-width: 1023px){.is-invisible-touch{visibility:hidden !important}}@media screen and (min-width: 1024px){.is-invisible-desktop{visibility:hidden !important}}@media screen and (min-width: 1024px)and (max-width: 1215px){.is-invisible-desktop-only{visibility:hidden !important}}@media screen and (min-width: 1216px){.is-invisible-widescreen{visibility:hidden !important}}@media screen and (min-width: 1216px)and (max-width: 1407px){.is-invisible-widescreen-only{visibility:hidden !important}}@media screen and (min-width: 1408px){.is-invisible-fullhd{visibility:hidden !important}}.section{padding:3rem 1.5rem}@media screen and (min-width: 1024px){.section{padding:3rem 3rem}.section.is-medium{padding:9rem 4.5rem}.section.is-large{padding:18rem 6rem}}.footer{background-color:#fafafa;padding:3rem 1.5rem 6rem}
"""

    actual = parse(css_text, set(), set())

    assert_css(expected, actual)
