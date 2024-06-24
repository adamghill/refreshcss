from dataclasses import dataclass, field
from pathlib import Path

from refreshcss.html.file import File


@dataclass
class Site:
    classes: set = field(default_factory=set)
    elements: set = field(default_factory=set)
    ids: set = field(default_factory=set)

    def get_template_paths(self):
        # Override this is in a subclass for different implementations
        return []

    def parse(self) -> None:
        self.classes = set()
        self.ids = set()
        self.elements = set()

        for template_path in self.get_template_paths():
            file = File(template_path)
            self.classes |= file.classes
            self.elements |= file.elements
            self.ids |= file.ids

    def __repr__(self):
        return "Site()"


@dataclass
class DjangoSite(Site):
    def get_template_paths(self) -> list[Path]:
        """
        Get a list of template paths stored in Django template directories.

        From https://stackoverflow.com/a/70077633.
        """

        from django import template

        directories: list[str] = []

        if hasattr(template, "loader"):
            for engine in template.loader.engines.all():
                # Exclude pip installed site package template directories
                directories.extend(
                    directory for directory in engine.template_dirs if "site-packages" not in str(directory)
                )

        files: list[Path] = []

        for directory in directories:
            files.extend(path for path in Path(directory).glob("**/*.htm?") if path)

        return files


@dataclass
class UrlSite(Site):
    """A site that is represented by a URL.

    TODO: Rename `File` to something more generic since it could be represented by URL paths.
    """

    def get_template_paths(self) -> list[Path]:
        """Get template paths for the site."""

        raise NotImplementedError()


@dataclass
class DirectorySite(Site):
    """A site that is represented by a directory."""

    def get_template_paths(self) -> list[Path]:
        """Get template paths for the directory."""

        raise NotImplementedError()
