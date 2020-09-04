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
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('exts'))


# -- Project information -----------------------------------------------------

project = 'utils'
copyright = '2020, GCPDS - utils'
author = 'GCPDS'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',

    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'IPython.sphinxext.ipython_console_highlighting',
]

naoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The master toctree document.
master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'page_width': '1080px',
    'sidebar_width': '310px',

    # 'fixed_sidebar': True,

    # 'show_relbars': True,
    # 'show_relbar_bottom': True,


    # 'github_user': 'bitprophet',
    # 'github_repo': 'alabaster',
}


html_sidebars = {
    '**': [
        'sidebar.html',
        # 'globaltoc.html',
        'navigation.html',
        'relations.html',
        # sourcelink.html
        'searchbox.html',
        # 'donate.html',
    ]
}

htmlhelp_basename = 'GCPDSdoc'


autodoc_mock_imports = [

    'IPython',
    'numpy',
    'scipy',
    'mne',
    'matplotlib',
    'google',
    'colorama',
    'tqdm',
    'pandas',
    'tables',

    # 'base_server.WSHandler_Serial',
    # 'base_server.WSHandler_WiFi',
    # 'ws.base_server',

]

todo_include_todos = True

# html_logo = '_static/logo.svg'
# html_favicon = '_static/favico.ico'


def setup(app):
    app.add_stylesheet("custom.css")


notebooks = os.listdir(os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '_notebooks'))

index = []
for notebook in notebooks:
    if notebook != 'readme.rst' and notebook.endswith('.rst'):
        index.append(f"_notebooks/{notebook.replace('.rst', '')}")

index = sorted(index)

with open('index.rst', 'w') as file:
    file.write("""
.. include:: _notebooks/readme.rst

Navigation
^^^^^^^^^^

.. toctree::
   :maxdepth: 2
   :name: mastertoc

   {index}



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

    """.format(index='\n   '.join(index)))
