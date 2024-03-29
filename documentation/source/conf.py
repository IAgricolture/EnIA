# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EnIA'
copyright = '2023, Pierluigi Lambiase, Carmine Laudato, Francesco Maria Puca, Gerardo Frino, Maria Lombardi, Benedetto Scala, Francesco Fattorusso'
author = 'Pierluigi Lambiase, Carmine Laudato, Francesco Maria Puca, Gerardo Frino, Maria Lombardi, Benedetto Scala, Francesco Fattorusso'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinxcontrib.httpdomain', 'sphinxcontrib.autohttp.flask','sphinxcontrib.autohttp.flaskqref']

templates_path = ['_templates']
exclude_patterns = []

language = 'it'


import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src/logic')))
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
