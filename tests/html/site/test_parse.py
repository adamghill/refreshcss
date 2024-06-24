from tests.fixtures import *  # noqa: F403


def test_parse_parsed_paths(django_site):
    django_site.parse()

    actual = django_site.get_template_paths()

    assert len(actual) == 2


def test_parse_classes(django_site):
    expected = {
        "pos",
        "info",
        "table-container",
        "container",
        "footer",
        "callout",
        "is-6",
        "header",
        "subtitle",
        "digital-ocean",
        "section",
        "column",
        "last-commit",
        "table",
        "neg",
        "title",
        "columns",
        "is-4",
        "section-true",
    }

    django_site.parse()
    actual = django_site.classes

    assert expected == actual


def test_parse_ids(django_site):
    expected = {"content-section"}

    django_site.parse()
    actual = django_site.ids

    assert expected == actual


def test_parse_elements(django_site):
    expected = {
        "div",
        "img",
        "span",
        "p",
        "h1",
        "h2",
        "table",
        "th",
        "footer",
        "section",
        "html",
        "head",
        "tbody",
        "script",
        "a",
        "ul",
        "meta",
        "thead",
        "tr",
        "td",
        "link",
        "abbr",
        "style",
        "li",
        "title",
        "body",
        "tfoot",
    }

    django_site.parse()
    actual = django_site.elements

    assert expected == actual
