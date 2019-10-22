import textwrap

from setuptools import setup

setup(
    use_scm_version={
        "write_to": "src/pytest_print/version.py",
        "write_to_template": textwrap.dedent(
            '''
        """contains version information"""
        from __future__ import unicode_literals

        __version__ = "{version}"
        '''
        ).lstrip(),
    }
)
