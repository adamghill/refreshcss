import pytest
from refreshcss.html.file import File


@pytest.mark.parametrize(
    "html, expected",
    [
        ("<p class='section' style=''>", {"section"}),
        ("<p class='section-two' style=''>", {"section-two"}),
    ],
)
def test_file_get_classes_from_html(html, expected, monkeypatch):
    monkeypatch.setattr(File, "_get_text", lambda _: html)

    actual = File(None).classes

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
def test_file_get_classes_from_django_template_html(html, expected, monkeypatch):
    monkeypatch.setattr(File, "_get_text", lambda _: html)

    actual = File(None).classes

    assert expected == actual
