# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "loadcfg"
copyright = "2025, Daniel Korkin"
author = "Daniel Korkin"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Automatically document modules and members.
    "sphinx.ext.napoleon",  # Support for Google and NumPy style docstrings.
    "sphinx.ext.autosummary",  # Generate summary tables.
    "sphinx.ext.viewcode",  # Add links to highlighted source code.
    "sphinx.ext.intersphinx",  # Link to external project documentation.
    "sphinx_copybutton",  # Add a "copy" button to code blocks.
    "sphinx_autodoc_typehints",  # Automatically include type hints in documentation.
]

# Automatically generate autosummary pages.
autosummary_generate = True

# Napoleon settings for Google style docstrings.
napoleon_google_docstring = True
napoleon_numpy_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
