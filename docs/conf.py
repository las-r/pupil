# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Path setup -----------------------------------------------------

# Add your project directory to sys.path, so autodoc can find it.
# This assumes your main package is in the root or 'src/' directory.
sys.path.insert(0, os.path.abspath('..'))

# -- Project information --------------------------------------------

project = 'Your Project Name'
copyright = '2025, Your Name'
author = 'Your Name'

# -- General configuration ------------------------------------------

extensions = [
    'sphinx.ext.autodoc',            # Automatically document docstrings
    'sphinx.ext.napoleon',           # Support for NumPy/Google style docstrings
    'sphinx.ext.viewcode',           # Add links to source code
    'sphinx.ext.autosummary',        # Create summary pages
    'sphinx_autodoc_typehints',      # Better type hint display
    'myst_parser',                   # If you use Markdown (.md)
]

autosummary_generate = True
autodoc_typehints = "description"

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output ----------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Optional: Handle missing imports -------------------------------

# This prevents autodoc from crashing if your package isn't fully installed
autodoc_mock_imports = ['pupil']  # Add any other packages that may not be available
