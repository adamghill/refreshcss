from refreshcss.css.parser import parse
from tests.utils import assert_css, get_site


def test_parse_grouped_selectors(monkeypatch):
    # Rule should be kept because .used is used, even if .unused is not
    expected = """
.used, .unused { color: red; }
"""
    css_text = """
.used, .unused { color: red; }
.unused-only { color: blue; }
"""
    site = get_site(monkeypatch, classes={"used"})
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_combinators(monkeypatch):
    # .parent > .child: kept because both used
    # .parent + .sibling: dropped because sibling unused
    expected = """
.parent > .child { color: red; }
"""
    css_text = """
.parent > .child { color: red; }
.parent + .sibling { color: blue; }
"""
    site = get_site(monkeypatch, classes={"parent", "child"})
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_pseudo_classes(monkeypatch):
    # .btn:hover: kept because .btn used
    expected = """
.btn:hover { color: red; }
"""
    css_text = """
.btn:hover { color: red; }
.unused:hover { color: blue; }
"""
    site = get_site(monkeypatch, classes={"btn"})
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_pseudo_elements(monkeypatch):
    # .header::before: kept because .header used
    expected = """
.header::before { content: "x"; }
"""
    css_text = """
.header::before { content: 'x'; }
.unused::after { content: 'y'; }
"""
    site = get_site(monkeypatch, classes={"header"})
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_complex_attributes(monkeypatch):
    # input[type="text"]: kept because element 'input' is used (if purely element based)
    # or .field[data-active]: kept because .field used
    current_expected = """
input[type="text"] { border: 1px solid; }

.field[data-active] { color: red; }
"""
    # tinycss2 serialization might normalize quotes, let's allow flexibility or match exact output
    # tinycss2 usually outputs double quotes for attributes
    input_css = """
input[type="text"] { border: 1px solid; }
.field[data-active] { color: red; }
.unused[data-active] { color: blue; }
div[data-unused] { color: green; }
"""

    # We need to make sure 'input' element is used and 'div' is NOT used (or not in site)
    site = get_site(monkeypatch, classes={"field"}, elements={"input"})
    actual = parse(input_css, site)
    assert_css(current_expected, actual)


def test_parse_universal_selector(monkeypatch):
    expected = """
* { box-sizing: border-box; }
"""
    css_text = """
* { box-sizing: border-box; }
"""
    # Should be kept regardless of site content
    site = get_site(monkeypatch)
    actual = parse(css_text, site)
    assert_css(expected, actual)
