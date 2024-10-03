# Configuration file for the Sphinx documentation builder.

project = 'phonebook'
copyright = '2024, Amin Asef'
author = 'Amin Asef'
release = '1.0'

import sys
import os

sys.path.insert(0, os.path.abspath(r'C:\Users\ashik\OneDrive\Desktop\projects\phonebook2\phonebook_2'))

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'alabaster'
html_static_path = ['_static']
