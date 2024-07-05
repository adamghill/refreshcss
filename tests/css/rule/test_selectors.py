from refreshcss.css.rule import Rule
from refreshcss.css.selector import Selector


def test_basic():
    expected = {Selector("body")}

    actual = Rule("body { color: 'blue'; }").selectors

    assert expected == actual


def test_additional():
    expected = {Selector(".container"), Selector(".last-commit")}

    actual = Rule(
        """
.container,
.last-commit {
    margin-left: 0px;
}"""
    ).selectors

    assert expected == actual


def test_additional_2():
    expected = {
        Selector(value="td"),
        Selector(value=".table"),
        Selector(value=".is-warning"),
        Selector(value=".is-alert"),
        Selector(value="th"),
    }

    actual = Rule(
        ".table td.is-warning,.table th.is-alert{background-color:#ffe08a;border-color:#ffe08a;color:rgba(0,0,0,.7)}"
    ).selectors

    assert expected == actual


def test_multiple():
    expected = {Selector(".last-commit"), Selector(".header")}

    actual = Rule(
        """
.header.last-commit {
    min-width: 8em;
}"""
    ).selectors

    assert expected == actual


def test_descendant():
    expected = {Selector(".last-commit"), Selector(".header")}

    actual = Rule(
        """
.header .last-commit {
    min-width: 8em;
}"""
    ).selectors

    assert expected == actual


def test_multiple_descendants():
    expected = {Selector(".last-commit"), Selector(".header"), Selector(".container")}

    actual = Rule(
        """
.container .header .last-commit {
    min-width: 8em;
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
    expected = {Selector(".header"), Selector(".last-commit")}

    actual = Rule(
        """
.header + .last-commit {
    min-width: 8em;
}
"""
    ).selectors

    assert expected == actual


def test_child():
    expected = {Selector(".header"), Selector(".last-commit")}

    actual = Rule(
        """
.header > .last-commit {
    min-width: 8em;
}
"""
    ).selectors

    assert expected == actual


def test_precede():
    expected = {Selector(".header"), Selector(".last-commit")}

    actual = Rule(
        """
.header ~ .last-commit {
    min-width: 8em;
}"""
    ).selectors

    assert expected == actual


def test_column():
    expected = {Selector(".header"), Selector(".last-commit")}

    actual = Rule(
        """
.header || .last-commit {
    min-width: 8em;
}
"""
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


def test_bare_attribute():
    expected = {Selector("[aria-label]")}

    actual = Rule("[aria-label] { position: relative; }").selectors

    assert expected == actual


def test_bare_attribute_with_extra():
    expected = {Selector("[aria-label]"), Selector('[role~="tooltip"]')}

    actual = Rule('[aria-label][role~="tooltip"] { position: relative; }').selectors

    assert expected == actual


def test_element_attribute():
    # Unsure if we want to this or `Selector('div[lang="en"]')` or add attributes to `Selector`?
    expected = {Selector("div"), Selector('[lang="en"]')}

    actual = Rule('div[lang="en"] { position: relative; }').selectors

    assert expected == actual


def test_at_rule():
    # @ rules should not show up in selectors

    expected = set()

    actual = Rule('@charset "utf-8";').selectors

    assert expected == actual
