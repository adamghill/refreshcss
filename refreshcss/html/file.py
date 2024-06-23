import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union

ID_RE = re.compile(r"<([\w-]+)\s+[^>]*id=(?P<id>[^>]+)")
CLASS_RE = re.compile(r"<(?P<element>[\w-]+)\s+[^>]*class=(?P<class>[^>]+)")

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
    def elements(self):
        if not self._elements:
            self._elements = set()

            # This is weird, but the classes property also finds elements and prevents scanning every file 3 times with
            # regex
            self.classes  # noqa: B018

        return self._elements

    @property
    def classes(self):
        if not self._classes:
            self._classes = set()

            for match in re.finditer(CLASS_RE, self._get_text()):
                tag_name = match.group("element")
                self._elements.add(tag_name)

                css_class = match.group("class").strip()

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

    @property
    def ids(self):
        if not self._ids:
            self._ids = set()

            for match in re.finditer(ID_RE, self._get_text()):
                css_id = match.group("id").strip()

                css_id = re.sub(DJANGO_STATEMENT_RE, "", css_id)
                css_id = re.sub(DJANGO_VARIABLE_RE, "", css_id)

                potential_id_attribute_value = css_id

                if css_id.startswith("'"):
                    matching_single_quote = css_id.index("'", 1)

                    potential_id_attribute_value = css_id[1:matching_single_quote]
                elif css_id.startswith('"'):
                    matching_double_quote = css_id.index('"', 1)

                    potential_id_attribute_value = css_id[1:matching_double_quote]
                else:
                    # Assume that a space means it's a new attribute
                    potential_id_attribute_value = css_id.split(" ")[0]

                for c in potential_id_attribute_value.split(" "):
                    if c:
                        self._ids.add(c)

        return self._ids

    def __repr__(self):
        return f"File({self.path})"
