# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ASD Cognition"
copyright = "2026, Tzahi Taub"
author = "Tzahi Taub"

# Get version from pyproject.toml
pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
with pyproject_path.open("rb") as f:
    pyproject_data = tomllib.load(f)

release = pyproject_data["project"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
