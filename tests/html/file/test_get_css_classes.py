from uuid import uuid4

import pytest
from refreshcss.html.file import File


@pytest.mark.parametrize(
    "html, expected",
    [
        # this stinks, but not much to do when using regex
        ("<p class='{% if True %}section{% endif %}' style=''>", {"section"}),
        # this stinks, but not much to do when using regex
        ("<p class='{{ 'whatever'|upper }} section{% endif %}' style=''>", {"section"}),
    ],
)
def test_file_get_class_attribute_values_from_html(html, expected, monkeypatch):
    monkeypatch.setattr(File, "_get_text", lambda _: html)
    monkeypatch.setattr(File, "get_file_hash", lambda _: str(uuid4()))

    actual = File(None).get_class_attribute_values()

    assert expected == actual


@pytest.mark.parametrize(
    "html, expected",
    [
        # this stinks, but not much to do when using regex
        ("<p class='{% if True %}section{% endif %}' style=''>", {"section"}),
        # this stinks, but not much to do when using regex
        ("<p class='{{ 'whatever'|upper }} section{% endif %}' style=''>", {"section"}),
    ],
)
def test_file_get_class_attribute_values_from_django_template_html(html, expected, monkeypatch):
    monkeypatch.setattr(File, "_get_text", lambda _: html)
    monkeypatch.setattr(File, "get_file_hash", lambda _: str(uuid4()))

    actual = File(None).get_class_attribute_values()

    assert expected == actual
