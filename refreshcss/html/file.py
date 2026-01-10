import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from justhtml.parser import FragmentContext, JustHTML

from refreshcss.utils.path import read_text

DJANGO_STATEMENT_RE = re.compile(r"\{\%.*?\%\}")
DJANGO_VARIABLE_RE = re.compile(r"\{\{.*?\}\}")
TEMPLATE_TAG_RE = re.compile(rf"{DJANGO_STATEMENT_RE.pattern}|{DJANGO_VARIABLE_RE.pattern}")

# Pattern to find potential class names in template tags
# Matches quoted strings that look like CSS classes
CLASS_IN_TEMPLATE_RE = re.compile(r'["\']([a-zA-Z_-][a-zA-Z0-9_-]*)["\']')

# Regexes that handle template tags nested inside quotes for class and id attributes
CLASS_ATTR_RE = re.compile(
    r"\bclass\s*=\s*("
    r"\"(?:\{\{.*?\}\}|\{\%.*?\%\}|[^\"])*\""
    r"|"
    r"'(?:\{\{.*?\}\}|\{\%.*?\%\}|[^'])*'"
    r")",
    re.IGNORECASE | re.DOTALL,
)
ID_ATTR_RE = re.compile(
    r"\bid\s*=\s*("
    r"\"(?:\{\{.*?\}\}|\{\%.*?\%\}|[^\"])*\""
    r"|"
    r"'(?:\{\{.*?\}\}|\{\%.*?\%\}|[^'])*'"
    r")",
    re.IGNORECASE | re.DOTALL,
)


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
    def _dom(self):
        # Pre-process text to remove Django tags, which can confuse the HTML parser
        # (especially in attributes with nested quotes)
        clean_text = self.text
        clean_text = re.sub(DJANGO_STATEMENT_RE, " ", clean_text)
        clean_text = re.sub(DJANGO_VARIABLE_RE, " ", clean_text)

        # Heuristic: if it looks like a full document, parse as document
        text_lower = clean_text.lower()
        if "<html" in text_lower or "<!doctype" in text_lower:
            return JustHTML(clean_text, track_node_locations=True)

        # Otherwise parse as fragment (avoids auto-adding html/head/body)
        ctx = FragmentContext("body")
        return JustHTML(clean_text, fragment_context=ctx, track_node_locations=True)

    def _walk(self, node):
        yield node
        # Ensure we iterate children safely if they exist
        if getattr(node, "children", None):
            for child in node.children:
                yield from self._walk(child)

    @cached_property
    def elements(self):
        _elements = set()

        # Iterate all nodes
        for node in self._walk(self._dom.root):
            if hasattr(node, "name") and node.name:
                # Filter out special nodes and IMPLICIT nodes (no origin line)
                name = str(node.name)
                origin_line = getattr(node, "origin_line", None)

                # html node often lacks origin_line even if explicit, so we whitelist it
                if not name.startswith("#") and not name.startswith("!"):
                    if name == "html" or origin_line is not None:
                        _elements.add(name)

        return _elements

    @cached_property
    def classes(self):
        _classes = set()

        # Step 1: Extract potential classes from template tags/variables
        # ONLY look inside class attributes to avoid catching literal strings used in filters/tags
        # that aren't intended to be CSS classes (e.g. filter arguments).
        for attr_match in CLASS_ATTR_RE.finditer(self.text):
            # Strip the outer quotes
            attr_content = attr_match.group(1)[1:-1]

            for tag_match in TEMPLATE_TAG_RE.finditer(attr_content):
                template_tag = tag_match.group(0)

                # Look for quoted strings that could be class names
                for class_match in CLASS_IN_TEMPLATE_RE.finditer(template_tag):
                    _classes.add(class_match.group(1))

        # Step 2: Extract classes from the DOM (STATIC)
        # ...
        for node in self._walk(self._dom.root):
            # Check for attrs existence safely
            attrs = getattr(node, "attrs", None)
            if attrs and "class" in attrs:
                css_class = attrs["class"]
                if not css_class:
                    continue

                # Django tags are already cleaned in _dom pre-processing.
                for c in css_class.split():
                    if c:
                        _classes.add(c)

        return _classes

    @cached_property
    def ids(self):
        _ids = set()

        # Step 1: Extract potential ids from template tags/variables
        # ONLY look inside id attributes
        for attr_match in ID_ATTR_RE.finditer(self.text):
            # Strip the outer quotes
            attr_content = attr_match.group(1)[1:-1]

            for tag_match in TEMPLATE_TAG_RE.finditer(attr_content):
                template_tag = tag_match.group(0)

                # Look for quoted strings that could be class names
                for class_match in CLASS_IN_TEMPLATE_RE.finditer(template_tag):
                    _ids.add(class_match.group(1))

        # Step 2: Extract ids from the DOM (STATIC)
        for node in self._walk(self._dom.root):
            # Check for attrs existence safely
            attrs = getattr(node, "attrs", None)
            if attrs and "id" in attrs:
                css_id = attrs["id"]
                if not css_id:
                    continue

                # Django tags are already cleaned in _dom pre-processing.
                for c in css_id.split():
                    if c:
                        _ids.add(c)

        return _ids

    def __repr__(self):
        return f"File({self.path})"
