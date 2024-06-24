import pytest
from refreshcss.html.file import File


@pytest.mark.parametrize(
    "text, expected",
    [
        ("<p class='after-element' style=''>", {"after-element"}),
        ('<p class="double-quotes">', {"double-quotes"}),
        ("<p  class='after-multiple-spaces' style=''>", {"after-multiple-spaces"}),
        ("<p  class=no-quotes style=''>", {"no-quotes"}),
        ("<p id='example-id' class='after-id' style=''>", {"after-id"}),
        ("<p class='first-class'></p><p class='second-class'></p>", {"first-class", "second-class"}),
        ("<p class='first second'></p>", {"first", "second"}),
        ("<fake-element class='fake-element'></p>", {"fake-element"}),
        ("<element0 class='element-with-number'></p>", {"element-with-number"}),
    ],
)
def test_classes_from_html(text, expected):
    file = File(None)
    file.text = text

    actual = file.classes

    assert expected == actual


@pytest.mark.parametrize(
    "text, expected",
    [
        # this stinks, but not much to do when using regex
        ("<p class='{% if True %}section{% endif %}' style=''>", {"section"}),
        # this stinks, but not much to do when using regex
        ("<p class='{{ 'whatever'|upper }} section{% endif %}' style=''>", {"section"}),
    ],
)
def test_classes_from_django_template_html(text, expected):
    file = File(None)
    file.text = text

    actual = file.classes

    assert expected == actual


@pytest.mark.parametrize(
    "text, expected",
    [
        ("<p class='' style=''>", {"p"}),
        ('<div class="">', {"div"}),
        ("<fake-element class=''></p>", {"fake-element"}),
        ("<element0 class='element-with-number'></p>", {"element0"}),
    ],
)
def test_elements_from_html(text, expected):
    file = File(None)
    file.text = text

    actual = file.elements

    assert expected == actual


@pytest.mark.parametrize(
    "text, expected",
    [
        ("<p id='first' style=''>", {"first"}),
        ('<p id="double-quotes">', {"double-quotes"}),
        ("<p  id='after-multiple-spaces' style=''>", {"after-multiple-spaces"}),
        ("<p id=no-quotes style=''>", {"no-quotes"}),
        ("<p class='example-class' id='after-class' style=''>", {"after-class"}),
        ("<p id='first-id'></p><p id='second-id'></p>", {"first-id", "second-id"}),
        ("<fake-element id='fake-element'></p>", {"fake-element"}),
        ("<element0 id='element-with-number'></p>", {"element-with-number"}),
    ],
)
def test_ids_from_html(text, expected):
    file = File(None)
    file.text = text

    actual = file.ids

    assert expected == actual
