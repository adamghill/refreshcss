from refreshcss.css.parser_v1 import _remove_empty_media_queries

"""
@media screen and(min-width:1408px){ }
@media screen and(min-width:1408px){.b {}}
"""


def test_remove_empty_media_queries_empty():
    expected = ""
    css_text = "@media screen and(min-width:1408px){}"

    actual = _remove_empty_media_queries(css_text)

    assert expected == actual


def test_remove_empty_media_queries_blank():
    expected = ""
    css_text = "@media screen and(min-width:1408px) { }"

    actual = _remove_empty_media_queries(css_text)

    assert expected == actual


def test_remove_empty_media_queries_new_line():
    expected = ""
    css_text = """@media screen and(min-width:1408px){

    }"""

    actual = _remove_empty_media_queries(css_text)

    assert expected == actual


def test_remove_empty_media_queries_has_rule():
    expected = "@media screen and(min-width:1408px) { .class-one { padding: 0; }}"
    css_text = "@media screen and(min-width:1408px) { .class-one { padding: 0; }}"

    actual = _remove_empty_media_queries(css_text)

    assert expected == actual
