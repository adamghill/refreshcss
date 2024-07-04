from refreshcss.cli import cli
from refreshcss.html.site import DjangoSite
from refreshcss.main import RefreshCSS

__all__ = ["RefreshCSS", "DjangoSite"]


if __name__ == "__main__":
    cli()
