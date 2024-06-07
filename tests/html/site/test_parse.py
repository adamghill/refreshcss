from tests.fixtures import *  # noqa: F403


def test_parse_parsed_paths(site):
    site.parse()

    actual = site.template_paths

    assert len(actual) == 2


def test_parse_class_attribute_values(site):
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

    site.parse()

    actual = site.class_attribute_values

    assert expected == actual
