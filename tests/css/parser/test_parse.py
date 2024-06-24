from refreshcss.css.parser import parse

from tests.utils import assert_css, get_site


def test_parse(monkeypatch):
    expected = """
body { color: 'blue'; }

.test-1 { color: 'red'; }
"""

    css_text = """
body { color: 'blue'; }

.test-1 { color: 'red'; }

.test-2 { color: 'green'; }
"""

    site = get_site(monkeypatch, classes={"test-1"}, elements={"body"})

    actual = parse(css_text, site)

    assert_css(expected, actual)
