#!/usr/bin/env python3
import sys
from setuptools import setup, find_packages

major = sys.version_info[0]
minor = sys.version_info[1]

if major != 3 or not 6 <= minor < 11:
    sys.stderr.write("This installation medium is only for Python 3.6 .. 3.10 and later. You are running Python %s.%s.\n" % (major, minor))

if major == 3 and minor > 10:
    sys.stderr.write("Please install using trepan-xpy-x.y.z.tar.gz from https://github.com/Trepan-Debugger/trepan-xpy/releases\n")
    sys.exit(1)
elif major == 3 and 3 <= minor < 6:
    sys.stderr.write("Please install using trepan-xpy_33-x.y.z.tar.gz from https://github.com/Trepan-Debugger/trepan-xpy/releases\n")
    sys.exit(1)
elif major == 2:
    sys.stderr.write("Please install using trepan-xpy_2.4-x.y.z.tar.gz from https://github.com/Trepan-Debugger/trepan-xpy/releases\n")
    sys.exit(1)

# Get the package information used in setup().
from __pkginfo__ import (
    author,
    author_email,
    classifiers,
    entry_points,
    install_requires,
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
    install_requires=install_requires,
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
