from pathlib import Path

import click

from refreshcss.html.site import FilesSite
from refreshcss.main import RefreshCSS


@click.command()
@click.option("-o", "--output", help="Write to file instead of stdout.")
@click.option("-R", "-r", "--recursive", is_flag=True, help="Recursively search subdirectories listed.")
@click.argument("css",)
@click.argument("html", nargs=-1, required=True)
@click.version_option()
def cli(output, recursive, css, html):
    """Remove classes, ids, and element selectors not used in HTML from CSS."""
    css = Path(css).read_text()
    site = FilesSite(html, recursive)
    site.parse()
    refresh_css = RefreshCSS(site)
    with click.open_file(output or "-", "w") as f:
        f.write(refresh_css.clean(css))
