from compressor.filters import CallbackOutputFilter
from django.core.cache import cache

from refreshcss import RefreshCSS, Site

REFRESH_CSS_SITE_CACHE_KEY = "refreshcss:site"


def clean(css_text: str) -> str:
    site = cache.get(REFRESH_CSS_SITE_CACHE_KEY)

    if not site:
        site = Site()
        site.parse()

        cache.set(REFRESH_CSS_SITE_CACHE_KEY, site)

    return RefreshCSS(site=site).clean(css_text)


class RefreshCSSFilter(CallbackOutputFilter):
    callback = "refreshcss.filters.clean"
