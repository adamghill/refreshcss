import pytest
from refreshcss.css.at import At
from refreshcss.css.rule import Rule
from refreshcss.css.selector import Selector


def test_at_rule():
    expected = At('@charset "utf-8";')

    actual = Rule('@charset "utf-8";').at

    assert expected == actual
    assert actual.is_nested is False


def test_at_rule_regular_internal_rule():
    actual = Rule('@charset "utf-8";').at

    with pytest.raises(AttributeError) as exc:
        actual.internal_rule  # noqa: B018

    assert exc.exconly() == "AttributeError: Regular at-rules do not have an internal rule"


def test_nested_at_rule():
    expected = At("@media screen and (min-width: 1024px) { .container { max-width:960px } }")

    actual = Rule("@media screen and (min-width: 1024px) { .container { max-width:960px } }").at

    assert expected == actual
    assert actual.is_nested is True


def test_nested_at_rule_internal_rule():
    expected = Rule(".container { max-width:960px }")

    actual = Rule("@media screen and (min-width: 1024px) { .container { max-width:960px } }").at.internal_rule

    assert expected == actual
