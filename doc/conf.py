# flake8: noqa
# pylint: skip-file
from __future__ import absolute_import, unicode_literals

from datetime import date

from pytest_print import __version__

company = ""
name = "pytest-print"
project = name
copyright = f"{date.today().year}, {company}"
version = __version__
release = version
language = "en"

extensions = ["sphinx.ext.extlinks", "sphinx.ext.inheritance_diagram"]
extlinks = {"ticket": ("https://github.com/gaborbernat/pytest-print/issues/%s", "")}

source_suffix = ".rst"
master_doc = "index"

add_function_parentheses = True

html_theme = "alabaster"
html_static_path = ["static"]
html_theme_options = {
    "logo": "favicon.png",
    "github_button": False,
    "github_banner": False,
    "fixed_sidebar": True,
    "description": "print onto pytest output",
    "page_width": "auto",
    "sidebar_width": "200px",
    "sidebar_collapse": True,
    "extra_nav_links": {},
}
html_sidebars = {"**": ["about.html", "navigation.html", "relations.html", "searchbox.html"]}
html_title = f"{version} {company}"
html_short_title = f"{name} {version}"
html_last_updated_fmt = "YYYY-MM-dd HH:MM:SS.mm"
htmlhelp_basename = f"{name}doc"

pygments_style = "friendly"

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
inheritance_graph_attrs = dict(rankdir="TB", size='""')
graphviz_output_format = "svg"
