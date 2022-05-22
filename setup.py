from setuptools import setup


long_description = """
# Mumath
Mumath is a LATEX-like to MathML conversion tool written in Python.

It also includes Markdown extensions for inline `$...$` and blocks `$$...$$`
and a simple server for quick testing.

Install and open in browser:
```sh
$ pip install mumath
$ py -m mumath.server --open
```
"""

packages = setuptools.find_packages("mumath")

options = {
    "name": "mumath",
    "version": "1.1.0",
    "author": "::fourpoints",
    "description": "LATEX to MathML conversion tool",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/fourpoints/mumath",
    "packages": packages,
    "package_dir": {"": "src"},
    "classifiers": {
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    },
    "package_data": {
        "mumath": ["data/index.html"],
    },
    "install_requires": [],
    "extra_requires": {
        "markdown": ["markdown"],
    },
    "entry_points": {
        "markdown.extensions": [
            "mumath = mumath.markdown:MuMark",
            "mumath-inline = mumath.markdown:MuMarkInline",
        ]
    }
}

setup(**options)
