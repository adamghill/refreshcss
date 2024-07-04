# RefreshCSS 🫧

>Make your CSS so fresh, so clean.

`RefreshCSS` is a Python library that removes unused classes, ids, and element selectors from CSS.

[![All Contributors](https://img.shields.io/github/all-contributors/adamghill/refreshcss?color=ee8449&style=flat-square)](#contributors)

## 🔧 Installation

`pip install refreshcss`

or

`pip install refreshcss[cli]`

if you want to use the command-line interface.

## ⭐️ Features

- Python library to integrate in other Python projects
- Can be used as a filter with `django-compressor` as part of minifying CSS
- Can be used via command-line interface, for example in CI

### 🗜️ Integrate with django-compressor

Add `"refreshcss.filters.RefreshCSSFilter"` to `COMPRESS_FILTERS` in the Django settings file.

```python
COMPRESS_FILTERS = {
    "css": [
        "refreshcss.filters.RefreshCSSFilter",
        ...
    ],
    "js": [...],
}
```

### ⌨️ Command-line interface

```sh
Usage: refreshcss [OPTIONS] CSS HTML...

  Remove classes, ids, and element selectors not used in HTML from CSS.

Options:
  -o, --output FILENAME  Write to file instead of stdout.
  -R, -r, --recursive    Recursively search subdirectories listed.
  --encoding TEXT        Character encoding to use when reading files. If not
                         specified, the encoding will be guessed.
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

## 🤓 How does it work?

1. Catalogue classes, ids, and elements that are currently being used in found HTML templates
1. Catalogue classes, ids, and elements in a CSS stylesheet
1. Return new CSS stylesheet that only contains rules that are actively being used by the HTML

## 🧐 Why?

I wanted to have a filter for `django-compressor` that would purge unused CSS as part of the `compress` step when deploying for [`coltrane`](https://coltrane.readthedocs.io) apps. After dealing with a manual process and attempting to integrate https://purgecss.com and https://github.com/uncss/uncss I thought "this couldn't be that hard to do in Python".

Which is always the thought at the beginning of every side project... and is never accurate.

## 🙋 FAQ

### Will this work with SPAs?

`RefreshCSS` only inspects HTML, so if CSS classes are being changed client-side then it will not know about it.

### Does this work by crawling a website URL?

Currently no, although that is a possibility in the future.

### Does this support HTML written in the Django Template Language?

Yes! That was a primary reason I built my own solution. 😅 Jinja might also be possible to support with some small tweaks, although it is untested.

### Is this what people mean when they say "treeshaking"?

Maybe. 🤷

### I found a bug!

Thanks for trying `RefreshCSS` out! Please make a PR (pull request) with a small test that replicates the bug or, if that is not possible, create a [new discussion](https://github.com/adamghill/refreshcss/discussions/new?category=ideas).

## 🤘 Related libraries

### Node

- [uncss](https://github.com/uncss/uncss)
- [PurgeCSS](https://purgecss.com/)

### Python

- [treeshake](https://pypi.org/project/treeshake/): I unfortunately could not get this to work on my local environment
- [cssutils](https://pypi.org/project/cssutils/): This unfortunately seemed to choke on more modern CSS (when I tested on Bulma 1.0)
- [css-optomizer](https://github.com/hamzaehsan97/CSS-optomizer)

## 🙏 Thanks

- [Django](https://www.djangoproject.com)
- [django-compressor](https://django-compressor.readthedocs.io/)
- [CSS standards](https://www.w3.org/Style/CSS/)

## ❤️ Support

This project is supported by GitHub [Sponsors](https://github.com/sponsors/adamghill) and [Digital Ocean](https://m.do.co/c/617d629f56c0).

<p>
  <a href="https://m.do.co/c/617d629f56c0">
    <img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/SVG/DO_Logo_horizontal_blue.svg" width="201px">
  </a>
</p>

## 🥳 Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://git.boelz.eu/tmb/"><img src="https://avatars.githubusercontent.com/u/641522?v=4?s=100" width="100px;" alt="Tobias Bölz"/><br /><sub><b>Tobias Bölz</b></sub></a><br /><a href="#code-tobiasmboelz" title="Code">💻</a> <a href="#doc-tobiasmboelz" title="Documentation">📖</a> <a href="#test-tobiasmboelz" title="Tests">⚠️</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
