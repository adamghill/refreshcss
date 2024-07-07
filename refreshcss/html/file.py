import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from refreshcss.utils.path import read_text

ID_RE = re.compile(r"<([\w-]+)\s+[^>]*id=(?P<id>[^>]+)")
ELEMENT_RE = re.compile(r"<(?P<element>[\w-]+)")
CLASS_RE = re.compile(r"<[\w-]+\s+[^>]*class=(?P<class>[^>]+)")

DJANGO_STATEMENT_RE = re.compile(r"\{\%.*?\%\}")
DJANGO_VARIABLE_RE = re.compile(r"\{\{.*?\}\}")


@dataclass
class File:
    path: Path
    encoding: str | None

    def __init__(self, path: str | Path, encoding: str | None = None):
        if isinstance(path, str):
            path = Path(path)

        self.path = path
        self.encoding = encoding

    @cached_property
    def text(self):
        return read_text(self.path, encoding=self.encoding)

    @cached_property
    def elements(self):
        _elements = set()

        for match in re.finditer(ELEMENT_RE, self.text):
            element = match.group("element").strip()
            _elements.add(element)

        return _elements

    @cached_property
    def classes(self):
        _classes = set()

        for match in re.finditer(CLASS_RE, self.text):
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
                    _classes.add(c)

        return _classes

    @cached_property
    def ids(self):
        _ids = set()

        for match in re.finditer(ID_RE, self.text):
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
                    _ids.add(c)

        return _ids

    def __repr__(self):
        return f"File({self.path})"
