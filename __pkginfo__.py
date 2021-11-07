# Copyright (C) 2020-2021 Rocky Bernstein <rocky@gnu.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Debugger packaging information"""

# To the extent possible we make this file look more like a
# configuration file rather than code like setup.py. I find putting
# configuration stuff in the middle of a function call in setup.py,
# which for example requires commas in between parameters, is a little
# less elegant than having it here with reduced code, albeit there
# still is some room for improvement.

# Things that change more often go here.
copyright = """Copyright (C) 2020 Rocky Bernstein <rb@dustyfeet.com>."""
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Debuggers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10 ",
]

# The rest in alphabetic order
author = "Rocky Bernstein"
author_email = "rb@dustyfeet.com"
entry_points = {"console_scripts": ["trepan-xpy = trepanxpy.__main__:main"]}
ftp_url = None
install_requires = [
    "columnize >= 0.3.10",
    "nose>=1.0.0, <= 1.3.7",
    "pyficache >= 2.0.1",
    "x-python >= 1.4.0",
    "term-background >= 1.0.1",
    "trepan3k >= 1.2.8",
]
license = "GPL3"
mailing_list = "python-debugger@googlegroups.com"
modname = "trepanxpy"
py_modules = None
short_desc = "GDB-like Debugger for x-python in the Trepan family"

import os.path as osp


def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


def read(*rnames):
    return open(osp.join(get_srcdir(), *rnames)).read()


# version.py sets variable VERSION.
__version__ = None
exec(read("trepanxpy", "version.py"))
web = "http://github.com/rocky/python-xpy/"

# tracebacks in zip files are funky and not debuggable
zip_safe = False

long_description = read("README.md") + "\n"
