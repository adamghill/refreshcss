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


# def test_site_parse_benchmark(monkeypatch, benchmark):
#     site = Site()

#     benchmark(site.parse)

#     assert site.class_attribute_values


def test_refresh_css_clean(monkeypatch, benchmark):
    expected = """/*!bulma.iov0.9.3|MITLicense|github.com/jgthms/bulma*//*!GeneratedbyBulmaCustomizerv0.2.0|https://github.com/webmasterish/bulma-customizer*//*!minireset.cssv0.0.6|MITLicense|github.com/jgthms/minireset.css*/html,body,p,ol,ul,li,dl,dt,dd,blockquote,figure,fieldset,legend,textarea,pre,iframe,hr,h1,h2,h3,h4,h5,h6{margin:0;padding:0}h1,h2,h3,h4,h5,h6{font-size:100%;font-weight:normal}ul{list-style:none}button,input,select,textarea{margin:0}html{box-sizing:border-box}*,*::before,*::after{box-sizing:inherit}img,video{height:auto;max-width:100%}iframe{border:0}table{border-collapse:collapse;border-spacing:0}td,th{padding:0}td:not([align]),th:not([align]){text-align:inherit}html{background-color:#fff;font-size:16px;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;min-width:300px;overflow-x:hidden;overflow-y:scroll;text-rendering:optimizeLegibility;text-size-adjust:100%}article,aside,figure,footer,header,hgroup,section{display:block}body,button,input,optgroup,select,textarea{font-family:BlinkMacSystemFont,-apple-system,"SegoeUI","Roboto","Oxygen","Ubuntu","Cantarell","FiraSans","DroidSans","HelveticaNeue","Helvetica","Arial",sans-serif}code,pre{-moz-osx-font-smoothing:auto;-webkit-font-smoothing:auto;font-family:monospace}body{color:#4a4a4a;font-size:1em;font-weight:400;line-height:1.5}a{color:#485fc7;cursor:pointer;text-decoration:none}astrong{color:currentColor}a:hover{color:#363636}code{background-color:#f5f5f5;color:#da1039;font-size:.875em;font-weight:normal;padding:.25em.5em.25em}hr{background-color:#f5f5f5;border:none;display:block;height:2px;margin:1.5rem0}img{height:auto;max-width:100%}input[type=checkbox],input[type=radio]{vertical-align:baseline}small{font-size:.875em}span{font-style:inherit;font-weight:inherit}strong{color:#363636;font-weight:700}fieldset{border:none}pre{-webkit-overflow-scrolling:touch;background-color:#f5f5f5;color:#4a4a4a;font-size:.875em;overflow-x:auto;padding:1.25rem1.5rem;white-space:pre;word-wrap:normal}precode{background-color:transparent;color:currentColor;font-size:1em;padding:0}tabletd,tableth{vertical-align:top}tabletd:not([align]),tableth:not([align]){text-align:inherit}tableth{color:#363636}.px-2{padding-left:.5rem!important;padding-right:.5rem!important}
"""

    site = _get_site(monkeypatch, class_attribute_values={"px-2"})

    with open(f"{getcwd()}/tests/static/css/bulma-0.9.3.min.css") as f:
        actual = benchmark(RefreshCSS(site=site).clean, f.read())

    assert_css(expected, actual)
