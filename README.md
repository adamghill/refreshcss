# RefreshCSS

>Make your CSS so fresh, so clean. 🫧

`RefreshCSS` is a Python library that removes unused styles from CSS. It is designed to be used with `django-compressor`, but it can also be used standalone.

## 🔧 Installation

`pip install refreshcss`

## 🤓 How does it work?

1. Catalogue HTML attributes that are currently being used
1. Catalogue CSS rules
1. Return new CSS that only contains rules that are actively being used by the HTML

## 🧐 Why?

I wanted to have a filter for `django-compressor` that would purge unused CSS as part of the `compress`. After dealing with a manual process and attempting to integrate https://purgecss.com and https://github.com/uncss/uncss I thought "this couldn't be that hard".

Which is always the thought at the beginning of every side project.

## 🙋 FAQ

### Will this work with SPAs?

`RefreshCSS` only inspects HTML, so if CSS classes are being changed client-side then it will not know about it.

### Does this work by crawling a website URL?

Currently no, although that is a possibility in the future.

### Does this support the HTML written in the Django Template Language?

Yes! That was a primary reason I built my own solution. 😅 Jinja might also be possible to support with some small tweaks, although I have not tested it.
