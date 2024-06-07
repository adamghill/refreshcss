from dataclasses import dataclass, field
from pathlib import Path

from refreshcss.html.file import File


@dataclass
class Site:
    class_attribute_values: set = field(default_factory=set)
    id_attribute_values: set = field(default_factory=set)
    template_paths: dict = field(default_factory=dict)

    def __init__(self, *template_path: str | Path):
        self.class_attribute_values = set()
        self.id_attribute_values = set()
        self.template_paths = {}
        self._file_paths = template_path

    def get_django_template_paths(self) -> list[Path]:
        """
        Get a list of template paths based on what was passed in to the constructor or default
        to the templates stored in Django template directories.

        From https://stackoverflow.com/a/70077633.
        """

        from django import template

        if self._file_paths:
            return self._file_paths

        directories: list[str] = []

        for engine in template.loader.engines.all():
            # Exclude pip installed site package template directories
            directories.extend(directory for directory in engine.template_dirs if "site-packages" not in str(directory))

        files: list[Path] = []

        for directory in directories:
            files.extend(path for path in Path(directory).glob("**/*.htm?") if path)

        return files

    def parse(self) -> None:
        self.template_paths = {}

        for template_path in self.get_django_template_paths():
            file = File(template_path)

            if (
                template_path not in self.template_paths
                or self.template_paths[template_path].file_hash != file.file_hash
            ):
                file.parse()

            self.template_paths[template_path] = file
            self.class_attribute_values |= file.class_attribute_values

    def __repr__(self):
        return "Site()"
