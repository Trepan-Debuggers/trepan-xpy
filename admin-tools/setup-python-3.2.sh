#!/bin/bash
PYTHON_VERSION=3.2

trepan_xpy_owd=$(pwd)
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..
(cd ../python3-trepan && ./admin-tools/setup-python-3.2.sh) && \
    (cd ../x-python && ./admin-tools/setup-python-3.1.sh)
git checkout python-3.2-to-3.5 && pyenv local $PYTHON_VERSION && git pull
cd $trepan_xpy_owd
rm -v */.python-version || true
