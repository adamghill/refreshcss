from refreshcss.css.rule import Rule


def test_basic():
    expected = {"aria-label", "role"}

    actual = Rule('[aria-label][role~="tooltip"] { position: relative; }').attributes

    assert expected == actual
