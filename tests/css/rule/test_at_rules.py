import pytest
from refreshcss.css.at import At
from refreshcss.css.rule import Rule


def test_at_rule():
    expected = {At('@charset "utf-8";')}

    actual = Rule('@charset "utf-8";').ats

    assert expected == actual


def test_at_rule_regular_is_nested():
    actual = next(iter(Rule('@charset "utf-8";').ats))

    assert actual.is_nested is False


def test_at_rule_regular_internal_rule():
    actual = next(iter(Rule('@charset "utf-8";').ats))

    # assert actual.is_nested is False

    with pytest.raises(AttributeError) as exc:
        actual.internal_rule  # noqa: B018

    assert exc.exconly() == "AttributeError: Regular at-rules do not have an internal rule"
