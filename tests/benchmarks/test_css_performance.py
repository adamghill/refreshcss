from tests.utils import get_site

from refreshcss.css.parser import parse


def test_css_parser_performance_bulma(monkeypatch, benchmark):
    """Benchmark CSS parsing performance with Bulma."""
    site = get_site(monkeypatch, classes={"container", "button", "navbar", "px-2", "table"})

    with open("tests/static/css/bulma-0.9.3.min.css") as f:
        css_text = f.read()

    benchmark(parse, css_text, site)


def test_css_parser_performance_simple(monkeypatch, benchmark):
    """Benchmark CSS parsing performance with a simple file."""
    site = get_site(monkeypatch, classes={"container"})

    with open("tests/static/css/styles.css") as f:
        css_text = f.read()

    benchmark(parse, css_text, site)
