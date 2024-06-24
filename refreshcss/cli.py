from pathlib import Path

import click

from refreshcss.html.site import FilesSite
from refreshcss.main import RefreshCSS


@click.command()
@click.option("--output", "-o", help="Write to file instead of stdout")
@click.argument("css",)
@click.argument("html", nargs=-1, required=True)
@click.version_option()
def cli(output, css, html):
    """Remove classes, ids, and element selectors not used in HTML from CSS."""
    css = Path(css).read_text()
    site = FilesSite(html)
    site.parse()
    refresh_css = RefreshCSS(site)
    with click.open_file(output or "-", "w") as f:
        f.write(refresh_css.clean(css))
