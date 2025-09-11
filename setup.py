#!/usr/bin/env python3
import sys
from setuptools import setup, find_packages


SYS_VERSION = sys.version_info[0:2]
if not ((3, 2) <= SYS_VERSION < (3, 6)):
    mess = "Python Versions 3.2 to 3.5 are supported in this branch this package."
    if SYS_VERSION >= (3, 11):
        mess += "\nFor your Python, version %s, use the master branch or a package created from that" % sys.version[0:3]
    if (3, 5) <= SYS_VERSION < (3, 11):
        mess += "\nFor your Python, version %s, use the python-3.6-to-3.10 branch or a package created from that" % sys.version[0:3]
    elif SYS_VERSION == (2, 7):
        mess += "\nFor your Python, version %s, use branch python-2.7 or a package created from that" % sys.version[0:3]
    print(mess)
    raise Exception(mess)

# Get the package information used in setup().
from __pkginfo__ import (
    author,
    author_email,
    classifiers,
    entry_points,
    extras_require,
    install_requires,
    license,
    long_description,
    modname,
    py_modules,
    short_desc,
    __version__,
    web,
    zip_safe,
)

__import__("pkg_resources")

packages = find_packages()

setup(
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    description=short_desc,
    entry_points=entry_points,
    extras_require=extras_require,
    install_requires=install_requires,
    license=license,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=modname,
    packages=packages,
    py_modules=py_modules,
    test_suite="nose.collector",
    url=web,
    version=__version__,
    zip_safe=zip_safe,
)
