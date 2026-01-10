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
        ("<p class='{% if True %}section{% endif %}' style=''>", {"section"}),
        ("<p class='{{ 'whatever'|upper }} section{% endif %}' style=''>", {"section", "whatever"}),
        ('<div class="{% block css_class %}default{% endblock %}"></div>', {"default"}),
        # Literal strings outside of a class attribute should be ignored
        ("{% sort 'last_commit' %}", set()),
        # Literal strings inside a template tag that is inside a class attribute should be caught
        ('<div class="{{ "extra-class"|default:"none" }}"></div>', {"extra-class", "none"}),
        # Keywords should NO LONGER be filtered out if explicitly quoted in a class attribute
        ('<div class="{% if "if" %}active{% endif %}"></div>', {"active", "if"}),
        # Mixed quotes
        ('<div class="{% if \'test-active\' == "test-active" %}active{% endif %}"></div>', {"active", "test-active"}),
        # Multiple classes in one tag
        ('<div class="{% cycle "first" "second" %}"></div>', {"first", "second"}),
        # Whitespace handling
        ('<div class="  {% if True %}  active  {% endif %}  "></div>', {"active"}),
        # Uppercase CLASS attribute
        ('<div CLASS="{% if True %}uppercase{% endif %}"></div>', {"uppercase"}),
        # ID attribute
        ('<div id="{% if True %}main-id{% endif %}"></div>', set()),  # Should be empty for classes property
    ],
)
def test_classes_from_django_template_html(text, expected):
    file = File(None)
    file.text = text

    actual = file.classes

    assert expected == actual


def test_classes_from_django_block_outside_attribute():
    # Test that template blocks outside of a class attribute are NOT caught
    text = '{% block content %}<div class="container"></div>{% endblock %}'
    file = File(None)
    file.text = text
    assert "container" in file.classes
    assert "content" not in file.classes


@pytest.mark.parametrize(
    "text, expected",
    [
        ("<div id='{% if True %}main{% endif %}'></div>", {"main"}),
        ("<div id='{{ 'unique' }}'></div>", {"unique"}),
        # Literal strings outside of an id attribute should be ignored
        ("{% sort 'last_commit' %}", set()),
    ],
)
def test_ids_from_django_template_html(text, expected):
    file = File(None)
    file.text = text

    actual = file.ids

    assert expected == actual


@pytest.mark.parametrize(
    "text, expected",
    [
        ("<div id='{% if True %}main{% endif %}'></div>", {"main"}),
        ("<div id='{{ 'unique' }}'></div>", {"unique"}),
        # ID as class should be ignored in IDs
        ("<div class='{% if True %}not-an-id{% endif %}'></div>", set()),
        # Uppercase ID attribute
        ('<div ID="{% if True %}UPPER-ID{% endif %}"></div>', {"UPPER-ID"}),
    ],
)
def test_ids_from_django_template_html_more(text, expected):
    file = File(None)
    file.text = text

    actual = file.ids

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
