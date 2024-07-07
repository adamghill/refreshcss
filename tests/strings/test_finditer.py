from refreshcss.utils.string import finditer


def test_finditer():
    expected = [(10, 13)]
    actual = list(finditer("fox", "the quick fox jumped over the hedge"))

    assert expected == actual


def test_finditer_2():
    expected = [(81, 104)]
    actual = list(
        finditer(
            "table th{color:#363636}",
            "pre code{background-color:transparent;color:currentColor;font-size:1em;padding:0}table th{color:#363636}",
        )
    )

    assert expected == actual


def test_finditer_3():
    expected = [(0, 81)]
    actual = list(
        finditer(
            "pre code{background-color:transparent;color:currentColor;font-size:1em;padding:0}",
            "pre code{background-color:transparent;color:currentColor;font-size:1em;padding:0}table th{color:#363636}",
        )
    )

    assert expected == actual
