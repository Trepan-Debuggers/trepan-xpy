#!/usr/bin/env python3
import sys

SYS_VERSION = sys.version_info[0:2]
if not ((3, 1) <= SYS_VERSION <= (3, 8)):
    mess = "Python Versions 3.1 to 3.8 are supported only in this package."
    if (2, 4) <= SYS_VERSION <= (2, 7):
        mess += "\nFor your Python, version %s, See trepan2" % sys.version[0:3]
    elif SYS_VERSION < (2, 4):
        mess += "\nFor your Python, version %s, see pydb" % sys.version[0:3]
    print(mess)
    raise Exception(mess)

# Get the package information used in setup().
from __pkginfo__ import (
    author,
    author_email,
    classifiers,
    entry_points,
    install_requires,
    license,
    long_description,
    modname,
    py_modules,
    short_desc,
    VERSION,
    web,
    zip_safe,
)

__import__("pkg_resources")

from setuptools import setup, find_packages

packages = find_packages()

setup(
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    description=short_desc,
    entry_points=entry_points,
    install_requires=install_requires,
    license=license,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=modname,
    packages=packages,
    py_modules=py_modules,
    test_suite="nose.collector",
    url=web,
    version=VERSION,
    zip_safe=zip_safe,
)
