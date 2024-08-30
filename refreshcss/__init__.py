from refreshcss.html.site import DjangoSite, PathSite
from refreshcss.main import RefreshCSS

__all__ = ["RefreshCSS", "DjangoSite", "PathSite"]

try:
    from refreshcss.cli import cli
except ImportError:
    pass
else:
    if __name__ == "__main__":
        cli()
