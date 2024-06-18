from refreshcss.css.parser import parse as parse_css
from refreshcss.css.parser_v2 import parse as parse_v2
from refreshcss.html.site import Site


class RefreshCSS:
    def __init__(self, site=None):
        self.site = site

        if not self.site:
            self.site = Site()
            self.site.parse()

    def clean(self, css_text: str) -> str:
        fresh_css_text = parse_css(css_text, self.site.class_attribute_values, self.site.id_attribute_values)

        return fresh_css_text

    def clean_v2(self, css_text: str) -> str:
        fresh_css_text = parse_v2(css_text, self.site.class_attribute_values, self.site.id_attribute_values)

        return fresh_css_text
