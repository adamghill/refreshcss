from refreshcss.css.rule import Rule


def test_basic():
    expected = {"container"}

    actual = Rule(
        """
#container {
    margin-left: 0px;
}"""
    ).ids

    assert expected == actual
