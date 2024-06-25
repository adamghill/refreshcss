from refreshcss.css.rule import Rule


def test_basic():
    expected = {"body"}

    actual = Rule(
        """
body {
    margin-left: 0px;
}"""
    ).elements

    assert expected == actual
