from refreshcss.css.parser import parse
from refreshcss.html.site import Site


class RefreshCSS:
    def __init__(self, site: Site):
        self.site = site

    def clean(self, css_text: str) -> str:
        fresh_css_text = parse(css_text, self.site)

        return fresh_css_text
