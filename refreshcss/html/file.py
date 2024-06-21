import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

CLASS_RE = re.compile(r"<(\w+)\sclass=([^>]+)")

DJANGO_STATEMENT_RE = re.compile(r"\{\%.*?\%\}")
DJANGO_VARIABLE_RE = re.compile(r"\{\{.*?\}\}")


@dataclass
class File:
    path: Path

    def __init__(self, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)

        self.path = path

        self._text = None
        self._classes = set()
        self._ids = set()
        self._elements = set()

    def _get_text(self):
        if not self._text:
            self._text = self.path.read_text()

        return self._text

    @property
    def classes(self):
        if not self._classes:
            self._classes = set()

            for match in re.finditer(CLASS_RE, self._get_text()):
                # tag_name = match.groups()[0]
                css_class = match.groups()[1].strip()

                css_class = re.sub(DJANGO_STATEMENT_RE, "", css_class)
                css_class = re.sub(DJANGO_VARIABLE_RE, "", css_class)

                potential_class_attribute_value = css_class

                if css_class.startswith("'"):
                    matching_single_quote = css_class.index("'", 1)

                    potential_class_attribute_value = css_class[1:matching_single_quote]
                elif css_class.startswith('"'):
                    matching_double_quote = css_class.index('"', 1)

                    potential_class_attribute_value = css_class[1:matching_double_quote]
                else:
                    # Assume that a space means it's a new attribute
                    potential_class_attribute_value = css_class.split(" ")[0]

                for c in potential_class_attribute_value.split(" "):
                    if c:
                        self._classes.add(c)

        return self._classes

    def __repr__(self):
        return f"File({self.path})"
