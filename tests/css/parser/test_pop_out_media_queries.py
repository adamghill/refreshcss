from refreshcss.css.parser_v1 import _pop_media_queries_out

from tests.utils import assert_css


def test_pop_media_queries_out_1():
    expected = """
    .one {
        display: none;
    }
"""

    css_text = """@media screen and (min-width: 1px) {
    .one {
        display: none;
    }
}
"""

    actual = _pop_media_queries_out(css_text)

    assert_css(expected, actual)


def test_pop_media_queries_out_2():
    expected = """
    .one {
        display: none;
    }
    .two {
        display: none;
    }
"""

    css_text = """@media screen and (min-width: 1px) {
    .one {
        display: none;
    }
    .two {
        display: none;
    }
}
"""

    actual = _pop_media_queries_out(css_text)

    assert_css(expected, actual)


def test_pop_media_queries_out_3():
    expected = """.before {
    display: none;
}

    .one {
        display: none;
    }
    .two {
        display: none;
    }
"""

    css_text = """.before {
    display: none;
}
@media screen and (min-width:1px) {
    .one {
        display: none;
    }
    .two {
        display: none;
    }
}
"""

    actual = _pop_media_queries_out(css_text)

    assert_css(expected, actual)


def test_pop_media_queries_out_4():
    expected = """.is-section-one {
    padding: 10px;
}

    .section {
        padding: 3rem 3rem
    }
    .section.is-medium {
        padding: 9rem 4.5rem
    }
    .section.is-large {
        padding: 18rem 6rem
    }

.is-section-two {
    padding: 10px;
}
"""

    css_text = """.is-section-one {
    padding: 10px;
}

@media screen and (min-width: 1024px) {
    .section {
        padding: 3rem 3rem
    }
    .section.is-medium {
        padding: 9rem 4.5rem
    }
    .section.is-large {
        padding: 18rem 6rem
    }
}

.is-section-two {
    padding: 10px;
}
"""

    actual = _pop_media_queries_out(css_text)
    print(actual)

    assert_css(expected, actual)


def test_pop_media_queries_out_5():
    expected = """
  .is-visibility-hidden-fullhd,
  .is-invisible-fullhd {
    visibility: hidden !important;
  }

  .is-shadowless {
    visibility: hidden !important;
  }
"""

    css_text = """@media screen and (min-width: 1408px) {
  .is-visibility-hidden-fullhd,
  .is-invisible-fullhd {
    visibility: hidden !important;
  }
}

@media screen and (max-width: 1408px) {
  .is-shadowless {
    visibility: hidden !important;
  }
}
"""

    actual = _pop_media_queries_out(css_text)
    print(actual)

    assert_css(expected, actual)
