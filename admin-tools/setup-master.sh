#!/bin/bash
PYTHON_VERSION=3.11

trepan_xpy_owd=$(pwd)
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..
(cd ../python-spark && git checkout master && pyenv local $PYTHON_VERSION && git pull);
(cd ../python-xdis && git checkout master && pyenv local $PYTHON_VERSION &&U git pull);
(cd ../../Trepan-Debuggers/python3-trepan && git checkout master && pyenv local $PYTHON_VERSION && git pull)
git checkout master &&  pyenv local $PYTHON_VERSION && git pull
cd $trepan_xpy_owd
