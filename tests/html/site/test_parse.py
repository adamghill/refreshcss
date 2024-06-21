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
