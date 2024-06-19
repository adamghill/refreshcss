from unittest.mock import ANY

from refreshcss.css.parser_v1 import _get_css_classes_and_ids


def test_get_css_classes_and_ids_one_class():
    expected = ({"class-one"}, ANY)
    actual = _get_css_classes_and_ids(".class-one { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_one_class_on_element():
    expected = ({"class-one"}, ANY)
    actual = _get_css_classes_and_ids("div.class-one { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_multiple_classes():
    expected = ({"class-one", "class-two"}, ANY)
    actual = _get_css_classes_and_ids(".class-one, .class-two { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_compound():
    expected = ({"class-one", "class-two"}, ANY)
    actual = _get_css_classes_and_ids(".class-one.class-two { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_child():
    expected = ({"class-one", "class-two"}, ANY)
    actual = _get_css_classes_and_ids(".class-one > .class-two { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_immediately_preceded():
    expected = ({"class-one", "class-two"}, ANY)
    actual = _get_css_classes_and_ids(".class-one + .class-two { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_preceded():
    expected = ({"class-one", "class-two"}, ANY)
    actual = _get_css_classes_and_ids(".class-one ~ .class-two { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_column():
    expected = ({"class-one", "class-two"}, ANY)
    actual = _get_css_classes_and_ids(".class-one || .class-two { display: none; }")

    assert expected == actual


def test_get_css_classes_and_ids_one_id():
    expected = (ANY, {"id-one"})
    actual = _get_css_classes_and_ids("#id-one { display: none; }")

    assert expected == actual


def test_get_css_class_and_ids_minified():
    expected = ({"is-unselectable"}, ANY)
    actual = _get_css_classes_and_ids(
        ".is-unselectable{-webkit-touch-callout:none;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}"
    )

    assert expected == actual


def test_get_css_class_and_ids_1():
    expected = ({"px-2"}, ANY)
    actual = _get_css_classes_and_ids(".px-2{padding-left:.5rem !important;padding-right:.5rem !important}")

    assert expected == actual
