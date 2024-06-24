from refreshcss.html.site import Site


def _minify_css(txt: str) -> str:
    # Remove all spaces and new lines (even if it isn't valid CSS) because just trying see that the
    # actual content is the same
    return txt.replace(" ", "").replace("\n", "")


def assert_css(expected: str, actual: str, print_out: bool = True) -> None:
    minified_expected = _minify_css(expected)

    if print_out:
        print()
        print("`" + expected + "`")
        print(f"Expected size: {len(expected)}")

    minified_actual = _minify_css(actual)

    if print_out:
        print()
        print("`" + actual + "`")
        print(f"Actual size: {len(actual)}")

    assert minified_expected == minified_actual


def get_site(monkeypatch, classes=None, ids=None, elements=None):
    site = Site()
    monkeypatch.setattr(site, "parse", lambda _: None)

    if classes is None:
        classes = set()

    if ids is None:
        ids = set()

    if elements is None:
        elements = set()

    site.classes = classes
    site.ids = ids
    site.elements = elements

    return site
