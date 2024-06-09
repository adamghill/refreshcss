import re
from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
from typing import Optional, Union

# TODO: Use html.parser and look for class or id
CLASS_RE = re.compile(r"<(\w+)\sclass=([^>]+)")

DJANGO_STATEMENT_RE = re.compile(r"\{\%.*?\%\}")
DJANGO_VARIABLE_RE = re.compile(r"\{\{.*?\}\}")


@dataclass
class File:
    path: Path
    file_hash: str
    class_attribute_values: set
    id_attribute_values: set
    # files: list
    # file_type: int  # TODO: enum: javascript / html
    _bytes: Optional[bytes]
    _text: Optional[str]

    def __init__(self, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)

        self.path = path
        self._bytes = None
        self._text = None

        self.file_hash = self.get_file_hash()

    def _get_bytes(self):
        if not self._bytes:
            self._bytes = self.path.read_bytes()

        return self._bytes

    def _get_text(self):
        if not self._text:
            self._text = self.path.read_text()

        return self._text

    def get_file_hash(self):
        return md5(self._get_bytes(), usedforsecurity=False).hexdigest()

    def get_class_attribute_values(self):
        class_attribute_values = set()

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
                    class_attribute_values.add(c)

        return class_attribute_values

    def parse(self):
        self.class_attribute_values = self.get_class_attribute_values()
        # TODO: get ids

    def __repr__(self):
        return f"File({self.path})"
