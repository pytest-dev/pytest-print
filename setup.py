# coding=utf-8
"""Handle the package management of the module"""
from __future__ import absolute_import

from setuptools import find_packages
from setuptools import setup

setup(
    name='pytest-print',
    use_scm_version=True,

    description='pytest plugin that provides a fixture to print onto the PyTest reporting',
    long_description=open("README.rst").read(),
    long_description_content_type='text/x-rst',
    author='Bernat Gabor',
    author_email='gaborjbernat@gmail.com',
    url='https://github.com/gaborbernat/pytest-print',

    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        "Framework :: Pytest"
    ],
    keywords='pytest print debug',
    project_urls={
        'Documentation': 'http://pytest-print.readthedocs.io/en/latest/',
        'Source': 'https://github.com/gaborbernat/pytest-print',
        'Tracker': 'https://github.com/gaborbernat/pytest-print/issues',
    },

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=False,

    entry_points={'pytest11': ['pytest_print = pytest_print']},

    platforms='any',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',

    install_requires=['pytest >= 3.0, <4',
                      'six >= 1.11.0, <2'],
    extras_require={
        ':python_version < "3.5"': [
            'typing >= 3.6.4, <4'
        ],
        'testing': ['pytest >= 3.5.0, < 4',
                    'coverage >= 4.5.1'],
        'lint': ['flake8 == 3.4.1',
                 'flake8-bugbear == 17.4.0',
                 'pre-commit == 1.8.2'],
        'docs': ['Sphinx >= 1.7.0, < 2']
    }
)
