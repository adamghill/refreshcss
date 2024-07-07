from refreshcss.utils.string import remove_string_at


def test_remove_string_at():
    expected = "the fox jumped over the hedge"
    actual = remove_string_at("the quick fox jumped over the hedge", 4, 10)

    assert expected == actual
