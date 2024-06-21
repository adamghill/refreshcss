from tests.fixtures import *  # noqa: F403


def test_get_django_template_paths(django_site):
    actual = django_site.get_template_paths()

    assert len(actual) == 2
    filter(lambda p: p.name == "index.html", actual)
    filter(lambda p: p.name == "base.html", actual)
