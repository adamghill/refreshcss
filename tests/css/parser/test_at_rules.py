from refreshcss.css.parser import parse
from tests.utils import assert_css, get_site


def test_parse_nested_media(monkeypatch):
    expected = """
@media screen {
  @media (min-width: 500px) {
    .visible { display: block; }
  }
}
"""
    css_text = """
@media screen {
  @media (min-width: 500px) {
    .visible { display: block; }
    .hidden { display: none; }
  }
}
"""
    site = get_site(monkeypatch, classes={"visible"})
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_supports(monkeypatch):
    expected = """
@supports (display: grid) {
  .grid { display: grid; }
}
"""
    css_text = """
@supports (display: grid) {
  .grid { display: grid; }
  .unused { display: none; }
}
"""
    site = get_site(monkeypatch, classes={"grid"})
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_container_queries(monkeypatch):
    expected = """
@container (min-width: 700px) {
  .card { padding: 2rem; }
}
"""
    css_text = """
@container (min-width: 700px) {
  .card { padding: 2rem; }
  .unused { padding: 0; }
}
"""
    site = get_site(monkeypatch, classes={"card"})
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_keyframes(monkeypatch):
    # Keyframes should be kept as they are at-rules without standard selectors in the prelude
    # But usually keyframes shouldn't be filtered by "usage" unless we track animation names (which we don't yet)
    # The current parser logic treats unknown at-restrictions (like @keyframes) or at-rules without selectors as "keep".
    # However, @keyframes content blocks (0%, 100%, from, to) are technically qualified rules?
    # Let's see how tinycss2 parses them.
    # TinyCSS2 parses keyframes blocks as QualifiedRules, but their preludes are keyframe selectors (e.g. "0%").
    # Our extract logic will likely fail to find classes/ids/elements in "0%", so it returns empty.
    # Empty selectors -> Rule kept?
    # Our logic: `if not classes and not ids and not elements: return True`
    # So keyframes should be preserved.

    expected = """
@keyframes slidein {
  from { transform: translateX(0%); }
  to { transform: translateX(100%); }
}
"""
    css_text = """
@keyframes slidein {
  from { transform: translateX(0%); }
  to { transform: translateX(100%); }
}
"""
    site = get_site(monkeypatch)
    actual = parse(css_text, site)
    assert_css(expected, actual)


def test_parse_font_face(monkeypatch):
    expected = """
@font-face {
  font-family: "Open Sans";
  src: url("/fonts/OpenSans-Regular-webfont.woff2") format("woff2");
}
"""
    css_text = """
@font-face {
  font-family: "Open Sans";
  src: url("/fonts/OpenSans-Regular-webfont.woff2") format("woff2");
}
"""
    site = get_site(monkeypatch)
    actual = parse(css_text, site)
    assert_css(expected, actual)
