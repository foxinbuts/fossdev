"""Configuration file for the Sphinx documentation builder."""

import os
import sys

# Ensure src/ directory is accessible for autodoc
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
project = "Sales"
copyright = "2026, foxinbandage"
author = "foxinbandage"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]
html_theme_options = {
    "description": "Sales analytics domain library and CLI application",
    "page_width": "960px",
}
