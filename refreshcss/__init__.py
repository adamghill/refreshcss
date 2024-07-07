from refreshcss.cli import cli
from refreshcss.html.site import DjangoSite, PathSite
from refreshcss.main import RefreshCSS

__all__ = ["RefreshCSS", "DjangoSite", "PathSite"]


if __name__ == "__main__":
    cli()
