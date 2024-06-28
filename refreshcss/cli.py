import click

from refreshcss.html.site import FilesSite
from refreshcss.main import RefreshCSS


@click.command()
@click.option("-o", "--output", type=click.File("w"), default="-", help="Write to file instead of stdout.")
@click.option("-R", "-r", "--recursive", is_flag=True, help="Recursively search subdirectories listed.")
@click.argument("css", type=click.File())
@click.argument("html", type=click.Path(exists=True), nargs=-1, required=True)
@click.version_option()
def cli(output, recursive, css, html):
    """Remove classes, ids, and element selectors not used in HTML from CSS."""
    css_text = css.read()
    site = FilesSite(html, recursive)
    site.parse()
    refresh_css = RefreshCSS(site)
    output.write(refresh_css.clean(css_text))
