import click

from refreshcss.html.site import FilesSite
from refreshcss.main import RefreshCSS
from refreshcss.utils import read_text


@click.command()
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="-",
    help="Write to file instead of stdout.",
)
@click.option(
    "-R",
    "-r",
    "--recursive",
    is_flag=True,
    help="Recursively search subdirectories listed.",
)
@click.option(
    "--encoding",
    default=None,
    show_default=True,
    help="Character encoding to use when reading files. If not specified, the encoding will be guessed.",
)
@click.argument("css", type=click.Path(exists=True, dir_okay=False))
@click.argument("html", type=click.Path(exists=True), nargs=-1, required=True)
@click.version_option()
def cli(output, recursive, encoding, css, html):
    """Remove classes, ids, and element selectors not used in HTML from CSS."""
    try:
        css_text = read_text(css, encoding=encoding)
    except (ValueError, UnicodeDecodeError) as e:
        raise click.BadParameter(f"'{css}': {e}", param_hint="CSS") from e
    except LookupError as e:
        raise click.BadParameter(e, param_hint="encoding") from e

    site = FilesSite(html, recursive, encoding)
    site.parse()
    refresh_css = RefreshCSS(site)
    output.write(refresh_css.clean(css_text))
