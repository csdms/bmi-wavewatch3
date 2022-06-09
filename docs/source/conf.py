# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "bmi_wavewatch3"
copyright = "2022, Eric Hutton"
author = "Eric Hutton"

# The full version, including alpha/beta/rc tags
release = "0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_static_path = ["_static", "images"]

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "description": "WAVEWATCH III data in Python",
    "logo": "wavewatch3_logo.png",
    "logo_name": False,
    "github_user": "csdms",
    "github_repo": "bmi-wavewatch3",
    "extra_nav_links": {
        "WAVEWATCH III": "https://polar.ncep.noaa.gov/waves",
        "bmi-wavewatch3 @ GitHub": "https://github.com/csdms/bmi-wavewatch3/",
        "Contact Us": "https://github.com/csdms/bmi-wavewatch3/issues",
    },
}

html_sidebars = {
    "**": ["about.html", "searchbox.html", "navigation.html", "sidebaroutro.html"]
}
