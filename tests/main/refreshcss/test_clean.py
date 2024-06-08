from os import getcwd

from refreshcss import RefreshCSS
from refreshcss.html.site import Site

from tests.utils import assert_css


def _get_site(monkeypatch, class_attribute_values=None, id_attribute_values=None):
    site = Site()
    monkeypatch.setattr(site, "parse", lambda _: None)

    if class_attribute_values is None:
        class_attribute_values = set()

    if id_attribute_values is None:
        id_attribute_values = set()

    site.class_attribute_values = class_attribute_values
    site.id_attribute_values = id_attribute_values

    return site


def test_clean():
    expected = """td div.pos {
    color: green;
    width: 20px;
    font-weight: 700;
}
td div.neg {
    color: red;
    width: 20px;
    }
.table {
    border: 1px #ccc solid;
    }
.callout {
    border: 1px #ccc solid;
    background: #f2f2f2;
    margin: 0px 3rem 0px 3rem;
    border-radius: 1rem;
    padding: 2rem;
    }
.container {
    margin-left: 0px;
    }
.header.last-commit {
    min-width: 8em;
    }
.header {
    font-weight: bold;
    }
.info {
    cursor: help;
    color: grey;
    font-weight: normal;
    }
.info::before {
    content: '\\27AF  ';
    }
.digital-ocean {
    float: right;
    }
@media only screen and (max-width: 30em) {
    .digital-ocean {
        display: none;
    }
}"""

    with open(f"{getcwd()}/tests/static/css/styles.css") as f:
        actual = RefreshCSS().clean(f.read())

    assert ".callout" in actual
    assert_css(expected, actual)


def test_clean_bulma_1(monkeypatch):
    expected = """/*!bulma.iov0.9.3|MITLicense|github.com/jgthms/bulma*//*!GeneratedbyBulmaCustomizerv0.2.0|https://github.com/webmasterish/bulma-customizer*//*!minireset.cssv0.0.6|MITLicense|github.com/jgthms/minireset.css*/html,body,p,ol,ul,li,dl,dt,dd,blockquote,figure,fieldset,legend,textarea,pre,iframe,hr,h1,h2,h3,h4,h5,h6{margin:0;padding:0}h1,h2,h3,h4,h5,h6{font-size:100%;font-weight:normal}ul{list-style:none}button,input,select,textarea{margin:0}html{box-sizing:border-box}*,*::before,*::after{box-sizing:inherit}img,video{height:auto;max-width:100%}iframe{border:0}table{border-collapse:collapse;border-spacing:0}td,th{padding:0}td:not([align]),th:not([align]){text-align:inherit}html{background-color:#fff;font-size:16px;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;min-width:300px;overflow-x:hidden;overflow-y:scroll;text-rendering:optimizeLegibility;text-size-adjust:100%}article,aside,figure,footer,header,hgroup,section{display:block}body,button,input,optgroup,select,textarea{font-family:BlinkMacSystemFont,-apple-system,"SegoeUI","Roboto","Oxygen","Ubuntu","Cantarell","FiraSans","DroidSans","HelveticaNeue","Helvetica","Arial",sans-serif}code,pre{-moz-osx-font-smoothing:auto;-webkit-font-smoothing:auto;font-family:monospace}body{color:#4a4a4a;font-size:1em;font-weight:400;line-height:1.5}a{color:#485fc7;cursor:pointer;text-decoration:none}astrong{color:currentColor}a:hover{color:#363636}code{background-color:#f5f5f5;color:#da1039;font-size:.875em;font-weight:normal;padding:.25em.5em.25em}hr{background-color:#f5f5f5;border:none;display:block;height:2px;margin:1.5rem0}img{height:auto;max-width:100%}input[type=checkbox],input[type=radio]{vertical-align:baseline}small{font-size:.875em}span{font-style:inherit;font-weight:inherit}strong{color:#363636;font-weight:700}fieldset{border:none}pre{-webkit-overflow-scrolling:touch;background-color:#f5f5f5;color:#4a4a4a;font-size:.875em;overflow-x:auto;padding:1.25rem1.5rem;white-space:pre;word-wrap:normal}precode{background-color:transparent;color:currentColor;font-size:1em;padding:0}tabletd,tableth{vertical-align:top}tabletd:not([align]),tableth:not([align]){text-align:inherit}tableth{color:#363636}.px-2{padding-left:.5rem!important;padding-right:.5rem!important}
"""

    site = _get_site(monkeypatch, class_attribute_values={"px-2"})

    with open(f"{getcwd()}/tests/static/css/bulma-0.9.3.min.css") as f:
        actual = RefreshCSS(site=site).clean(f.read())

    assert_css(expected, actual)


def test_clean_bulma_2(monkeypatch):
    expected = ".px-2{padding-left:.5rem !important;padding-right:.5rem !important}"

    site = _get_site(monkeypatch, class_attribute_values={"px-2"})

    css_text = """.px-2 {
    padding-left:.5rem !important;
    padding-right:.5rem !important
}
.section {
    padding: 3rem 1.5rem
}
.footer {
    background-color: #fafafa; padding: 3rem 1.5rem 6rem
}"""

    actual = RefreshCSS(site=site).clean(css_text)

    assert_css(expected, actual)


def test_clean_bulma_3(monkeypatch):
    expected = ".px-2{padding-left:.5rem !important;padding-right:.5rem !important}"
    # ?asdf

    site = _get_site(monkeypatch, class_attribute_values={"px-2"})

    css_text = """.px-2 {
    padding-left:.5rem !important;
    padding-right:.5rem !important
}
.section {
    padding: 3rem 1.5rem
}
@media screen and (min-width: 1024px) {
    .section {
        padding: 3rem 3rem
    }
    .section.is-medium {
        padding: 9rem 4.5rem
    }
    .section.is-large {
        padding: 18rem 6rem
    }
}
.footer {
    background-color: #fafafa; padding: 3rem 1.5rem 6rem
}"""

    actual = RefreshCSS(site=site).clean(css_text)

    assert_css(expected, actual)


# def test_clean_bulma_3(monkeypatch):
#     expected = ""

#     site = Site()
#     monkeypatch.setattr(site, "parse", lambda _: None)
#     site.class_attribute_values = {"px-2"}

#     css_text = """.is-unselectable{-webkit-touch-callout:none;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.title:not(:last-child),.subtitle:not(:last-child),.table-container:not(:last-child),.table:not(:last-child){margin-bottom:1.5rem}.is-overlay{bottom:0;left:0;position:absolute;right:0;top:0}/*! minireset.css v0.0.6 | MIT License | github.com/jgthms/minireset.css */html,body,p,ol,ul,li,dl,dt,dd,blockquote,figure,fieldset,legend,textarea,pre,iframe,hr,h1,h2,h3,h4,h5,h6{margin:0;padding:0}h1,h2,h3,h4,h5,h6{font-size:100%;font-weight:normal}ul{list-style:none}button,input,select,textarea{margin:0}html{box-sizing:border-box}*,*::before,*::after{box-sizing:inherit}img,video{height:auto;max-width:100%}iframe{border:0}table{border-collapse:collapse;border-spacing:0}td,th{padding:0}td:not([align]),th:not([align]){text-align:inherit}html{background-color:#fff;font-size:16px;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;min-width:300px;overflow-x:hidden;overflow-y:scroll;text-rendering:optimizeLegibility;text-size-adjust:100%}article,aside,figure,footer,header,hgroup,section{display:block}body,button,input,optgroup,select,textarea{font-family:BlinkMacSystemFont,-apple-system,"Segoe UI","Roboto","Oxygen","Ubuntu","Cantarell","Fira Sans","Droid Sans","Helvetica Neue","Helvetica","Arial",sans-serif}code,pre{-moz-osx-font-smoothing:auto;-webkit-font-smoothing:auto;font-family:monospace}body{color:#4a4a4a;font-size:1em;font-weight:400;line-height:1.5}a{color:#485fc7;cursor:pointer;text-decoration:none}a strong{color:currentColor}a:hover{color:#363636}code{background-color:#f5f5f5;color:#da1039;font-size:.875em;font-weight:normal;padding:.25em .5em .25em}hr{background-color:#f5f5f5;border:none;display:block;height:2px;margin:1.5rem 0}img{height:auto;max-width:100%}input[type=checkbox],input[type=radio]{vertical-align:baseline}small{font-size:.875em}span{font-style:inherit;font-weight:inherit}strong{color:#363636;font-weight:700}fieldset{border:none}pre{-webkit-overflow-scrolling:touch;background-color:#f5f5f5;color:#4a4a4a;font-size:.875em;overflow-x:auto;padding:1.25rem 1.5rem;white-space:pre;word-wrap:normal}pre code{background-color:transparent;color:currentColor;font-size:1em;padding:0}table td,table th{vertical-align:top}table td:not([align]),table th:not([align]){text-align:inherit}table th{color:#363636}.container{flex-grow:1;margin:0 auto;position:relative;width:auto}.container.is-fluid{max-width:none !important;padding-left:32px;padding-right:32px;width:100%}@media screen and (min-width: 1024px){.container{max-width:960px}}@media screen and (max-width: 1215px){.container.is-widescreen:not(.is-max-desktop){max-width:1152px}}@media screen and (max-width: 1407px){.container.is-fullhd:not(.is-max-desktop):not(.is-max-widescreen){max-width:1344px}}@media screen and (min-width: 1216px){.container:not(.is-max-desktop){max-width:1152px}}@media screen and (min-width: 1408px){.container:not(.is-max-desktop):not(.is-max-widescreen){max-width:1344px}}.table{background-color:#fff;color:#363636}.table td,.table th{border:1px solid #dbdbdb;border-width:0 0 1px;padding:.5em .75em;vertical-align:top}.table td.is-white,.table th.is-white{background-color:#fff;border-color:#fff;color:#0a0a0a}.px-2{padding-left:.5rem !important;padding-right:.5rem !important}"""

#     actual = RefreshCSS(site=site).clean(css_text)

#     assert_css(expected, actual)
