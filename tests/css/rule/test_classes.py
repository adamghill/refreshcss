from refreshcss.css.rule import Rule


def test_basic():
    expected = {"container", "last-commit"}

    actual = Rule(
        """
.container,
.last-commit {
    margin-left: 0px;
}"""
    ).classes

    assert expected == actual
