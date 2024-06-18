from refreshcss.css.rule import Rule
from refreshcss.css.selector import Selector


def test_basic():
    expected = {Selector("body"), Selector(".test-1"), Selector(".test-2")}

    actual = Rule(
        """
body { color: 'blue'; }

.test-1 { color: 'red'; }

.test-2 { color: 'green'; }
"""
    ).selectors

    assert expected == actual


def test_additional():
    expected = {Selector(".container"), Selector(".last-commit"), Selector(".header")}

    actual = Rule(
        """
.container,
.last-commit {
    margin-left: 0px;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_multiple():
    expected = {Selector(".last-commit"), Selector(".header"), Selector(".container")}

    actual = Rule(
        """
.container {
    margin-left: 0px;
}
.header.last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_descendant():
    expected = {Selector(".last-commit"), Selector(".header"), Selector(".container")}

    actual = Rule(
        """
.container {
    margin-left: 0px;
}
.header .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_multiple_descendants():
    expected = {Selector(".last-commit"), Selector(".header"), Selector(".container")}

    actual = Rule(
        """
.container .header .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_pseudo():
    expected = {Selector(".header")}

    actual = Rule(
        """
.header:empty {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_sibling():
    expected = {Selector(".header"), Selector(".last-commit"), Selector(".container")}

    actual = Rule(
        """
.container {
    margin-left: 0px;
}
.header + .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_child():
    expected = {Selector(".header"), Selector(".last-commit"), Selector(".container")}

    actual = Rule(
        """
.container {
    margin-left: 0px;
}
.header > .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_precede():
    expected = {Selector(".header"), Selector(".last-commit"), Selector(".container")}

    actual = Rule(
        """
.container {
    margin-left: 0px;
}
.header ~ .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_column():
    expected = {Selector(".header"), Selector(".last-commit"), Selector(".container")}

    actual = Rule(
        """
.container {
    margin-left: 0px;
}
.header || .last-commit {
    min-width: 8em;
}
.header {
    font-weight: bold;
}"""
    ).selectors

    assert expected == actual


def test_bulma_css_1():
    expected = {Selector(".is-invisible-tablet-only")}

    actual = Rule(".is-invisible-tablet-only{visibility:hidden !important}").selectors

    assert expected == actual


def test_bulma_css_2():
    expected = {Selector(".is-clearfix")}

    actual = Rule('.is-clearfix::after{clear:both;content:" ";display:table}').selectors

    assert expected == actual
