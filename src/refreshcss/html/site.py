from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

from refreshcss.html.file import File


@dataclass
class Site:
    classes: set = field(default_factory=set, init=False)
    elements: set = field(default_factory=set, init=False)
    ids: set = field(default_factory=set, init=False)

    @property
    def encoding(self) -> str | None:
        return None

    def get_template_paths(self):
        # Override this is in a subclass for different implementations
        return []

    def parse(self) -> None:
        self.classes = set()
        self.ids = set()
        self.elements = set()

        for template_path in self.get_template_paths():
            file = File(template_path, self.encoding)
            self.classes |= file.classes
            self.elements |= file.elements
            self.ids |= file.ids

    def __repr__(self):
        return "Site()"


@dataclass
class DjangoSite(Site):
    @cached_property
    def encoding(self) -> str | None:
        from django.conf import settings

        return settings.DEFAULT_CHARSET

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
class PathSite(Site):
    """A site that is represented by a list of paths."""

    paths: Iterable[str] = field(default_factory=list)
    recursive: bool = field(default=False)
    encoding: str | None = field(default=None)

    def get_template_paths(self) -> Iterator[Path]:
        for path_str in self.paths:
            path = Path(path_str)

            if self.recursive:
                try:
                    yield from (p for p in path.rglob("*") if p.is_file())
                except OSError:
                    yield path
            else:
                yield path
