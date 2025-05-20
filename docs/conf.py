import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Pupil"
copyright = "2025, Nayif Ehan"
author = "Nayif Ehan"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
    "myst_parser"
]

autosummary_generate = True
autodoc_typehints = "description"

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

autodoc_mock_imports = ["pupil"]
