# AGENTS.md - RefreshCSS Library Analysis

## Overview

**RefreshCSS** is a pure Python library that removes unused CSS selectors (classes, ids, and elements) from CSS files based on what's actually used in HTML templates. It's designed to work seamlessly with Django/Jinja-style templates and can be integrated into build processes.

**Version**: 0.5.1  
**License**: MIT  
**Python**: 3.10+

## Core Purpose

RefreshCSS performs CSS "tree-shaking" or "purging" - it analyzes HTML templates to find which CSS selectors are actually being used, then outputs a cleaned CSS file containing only those selectors. This reduces CSS file size and improves performance.

## Architecture

### High-Level Flow

1. **Parse HTML** → Extract all classes, ids, and elements from HTML templates.
   - Uses **JustHTML** for static HTML structure.
   - Uses **Aggressive Regex Extraction** for classes and IDs inside Django/Jinja template tags (limited to `class` and `id` attributes).
2. **Parse CSS** → Extract all rules and selectors from CSS files using **tinycss2**.
3. **Compare** → Match CSS selectors against HTML usage using efficient set operations.
4. **Output** → Return cleaned CSS containing only used selectors, preserving comments and at-rules.

### Core Components

#### 1. HTML Parsing (`src/refreshcss/html/`)

**`File` class** (`html/file.py`):
- Parses individual HTML files using a combination of **JustHTML** and targeted regex.
- Extracts three types of selectors:
  - **Classes**: 
    - **Static**: Extracted via `JustHTML` from the DOM (template tags are replaced with spaces to avoid "smashing" adjacent classes).
    - **Aggressive**: Extracted from Django/Jinja template tags (e.g., `{{ ... }}`, `{% ... %}`) found strictly within `class="..."` HTML attributes.
  - **IDs**: 
    - **Static**: Extracted via `JustHTML`.
    - **Aggressive**: Extracted from template tags found strictly within `id="..."` HTML attributes.
  - **Elements**: Extracted via `JustHTML` tag name traversal.
- Uses cached properties for performance.

**Key Regex Patterns**:
- `CLASS_ATTR_RE`: Matches `class="..."` attributes, handling nested template tags and quotes.
- `ID_ATTR_RE`: Matches `id="..."` attributes.
- `TEMPLATE_TAG_RE`: Matches `{% ... %}` and `{{ ... }}`.
- `CLASS_IN_TEMPLATE_RE`: Matches quoted strings within template tags that look like CSS classes/IDs.

**`Site` classes** (`html/site.py`):
- **`Site`**: Abstract base class that aggregates classes, ids, and elements from multiple files
- **`DjangoSite`**: Automatically discovers Django template directories and uses Django's default charset
- **`PathSite`**: Accepts explicit file paths, supports recursive directory scanning
- **`UrlSite`**: Placeholder for future URL-based crawling (not yet implemented)

#### 2. CSS Parsing (`src/refreshcss/css/`)

**`parser.py`** (`css/parser.py`):
- Uses **tinycss2** to parse CSS into an AST-like stream of tokens and rules.
- **Key algorithm**:
  1. `tinycss2.parse_stylesheet` converts CSS to rules while preserving comments.
  2. For each **QualifiedRule** (regular CSS rule):
     - `_rule_is_kept` performs a single-pass scan over the selector prelude.
     - Short-circuits as soon as any selector in a comma-separated list is deemed "used".
     - Validates against `site.classes`, `site.ids`, and `site.elements`.
  3. For each **AtRule** (e.g., `@media`, `@container`, `@supports`):
     - Recursively filters nested rules.
     - Removes at-rules that become empty after filtering.
     - Preserves non-nested at-rules like `@font-face` or `@keyframes`.
  4. Serializes the kept rules back to CSS text.

**Special Cases Handled**:
- **Modern CSS**: Full support for nesting, container queries, and complex selectors via `tinycss2`.
- **Comments**: Preserved by default as they are included in the `tinycss2` rule list.
- **Universal selector (`*`)**: Always preserved.
- **Pseudo-elements/classes**: Correctly ignored during base-selector matching.

#### 3. Main Interface (`refreshcss/main.py`)

**`RefreshCSS` class**:
- Tie common logic together.
- The `clean()` method accepts CSS text and returns cleaned CSS.

#### 4. Utilities (`refreshcss/utils/`)

**`path.py`**:
- `read_text()`: Reads files with optional encoding detection using `charset-normalizer`.

**`string.py`**:
- `finditer()`: Yields start/end indices for substring matches
- `remove_string_at()`: Removes substring by index range

### Integration Points

#### 1. Command-Line Interface (`src/refreshcss/cli.py`)

Uses Click framework to provide a CLI:
```bash
refreshcss [OPTIONS] CSS HTML...

Options:
  -o, --output FILENAME  # Write to file instead of stdout
  -R, -r, --recursive    # Recursively search subdirectories
  --encoding TEXT        # Character encoding
```

**Example**:
```bash
refreshcss styles.css templates/ -r -o cleaned.css
```

#### 2. Django Compressor Filter (`src/refreshcss/filters.py`)

**`RefreshCSSFilter`**:
- Integrates with `django-compressor` as a filter.
- Caches the parsed `DjangoSite` object for performance.
- Automatically runs during `python manage.py compress`.

**Usage in Django settings**:
```python
COMPRESS_FILTERS = {
    "css": [
        "refreshcss.filters.RefreshCSSFilter",
    ],
}
```

## Key Design Decisions

### 1. Spec-Compliant Parsing
- **Why**: Moved from regex to **tinycss2** (CSS) and **JustHTML** (HTML) to ensure correctness with modern standards.
- **Trade-off**: Slightly higher execution cost for small files, but significantly faster for real-world CSS frameworks (Bulma is ~7x faster with `tinycss2`).

### 2. Context-Aware Aggressive Extraction
- **Why**: Extracts class names and IDs from template logic (e.g., `{% if ... %}`) but only within relevant HTML attributes.
- **Benefit**: Prevents false positives from filter arguments or other template code outside of `class` and `id` tags.

### 3. Build-System: UV
- **Why**: Utilizes `uv` and `uv_build` for extremely fast dependency management and building.
- **Layout**: Adopted the standard `src` layout for better package isolation and testing correctness.

### 4. Caching Strategy
- `File` class uses `@cached_property` for expensive parsing operations.
- Django filter caches the entire `DjangoSite` object to avoid re-parsing templates.

## Limitations & Known Issues

1. **Not suitable for SPAs**: Only inspects static HTML templates, not dynamically generated classes
2. **No URL crawling**: Cannot analyze live websites (yet - `UrlSite` is a placeholder)
3. **Regex limitations**: May struggle with extremely complex or unusual CSS syntax
4. **No JavaScript analysis**: Won't detect classes added/removed via JavaScript

## Testing Strategy

The library has comprehensive tests covering:
- HTML parsing (classes, ids, elements)
- CSS parsing (rules, selectors, at-rules)
- Integration tests with real CSS frameworks (Bulma 0.9.3)
- Edge cases (element/class name collisions, media queries)
- Benchmark tests for performance

Test files are organized by component:
- `tests/html/` - HTML parsing tests
- `tests/css/` - CSS parsing tests
- `tests/main/` - Integration tests
- `tests/benchmarks/` - Performance tests

## Performance Considerations

1. **Cached properties**: Expensive operations (regex matching) are cached
2. **Set operations**: Fast membership testing using Python sets
3. **Django filter caching**: Entire site is cached to avoid re-parsing on every CSS file
4. **Regex compilation**: Patterns are compiled once at module level

## Dependencies

**Core**:
- `tinycss2` - Spec-compliant CSS parsing
- `justhtml` - Spec-compliant HTML parsing

**Optional**:
- `click` - CLI interface (extras: `cli`)
- `charset-normalizer` - Encoding detection (extras: `cli`)

**Dev**:
- `pytest`, `pytest-django`, `pytest-cov`, `pytest-benchmark`
- `django`, `django-compressor`
- `ruff` - Linting and formatting
- `uv_build` - Build backend

## Use Cases

1. **Django projects**: Reduce CSS bundle size in production
2. **Static site generators**: Clean up CSS for static HTML sites
3. **CI/CD pipelines**: Automated CSS optimization
4. **Template-based frameworks**: Any Python web framework using templates

## Example Workflow

```python
from pathlib import Path
from refreshcss import RefreshCSS, PathSite

# 1. Define HTML template locations
site = PathSite(paths=["templates", "components"], recursive=True)

# 2. Parse all HTML files to extract selectors
site.parse()
# site.classes = {'container', 'header', 'button', ...}
# site.ids = {'main', 'nav', ...}
# site.elements = {'div', 'p', 'a', ...}

# 3. Read CSS file
css_text = Path("styles.css").read_text()

# 4. Clean CSS
refresher = RefreshCSS(site)
cleaned_css = refresher.clean(css_text)

# 5. Write output
Path("styles.min.css").write_text(cleaned_css)
```

## Future Enhancements (Based on TODO and Code)

1. **URL crawling**: Implement `UrlSite` to analyze live websites
2. **Better CSS parsing**: Create a `Stylesheet` class to encapsulate parsing logic
3. **Improved media query handling**: More sophisticated nested rule processing
4. **JavaScript analysis**: Detect dynamically added classes
5. **Source maps**: Track which HTML files use which CSS rules

## Related Projects

**Python**:
- `treeshake` - Similar concept but had compatibility issues
- `cssutils` - Struggles with modern CSS syntax
- `css-optimizer` - Alternative approach

**JavaScript/Node**:
- `PurgeCSS` - Popular Node.js solution
- `uncss` - Another Node.js alternative

RefreshCSS fills the gap for Python-based projects that want CSS optimization without adding Node.js to their build process.
