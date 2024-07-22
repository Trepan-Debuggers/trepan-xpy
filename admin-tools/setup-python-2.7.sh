#!/bin/bash
PYTHON_VERSION=2.7

export PATH=$HOME/.pyenv/bin/pyenv:$PATH
trepan_xpy_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..
(cd ../python3-trepan && ./admin-tools/setup-python-2.4.sh) && \
    (cd ../x-python && ./admin-tools/setup-python-2.7.sh)
git checkout python-2.7 && pyenv local $PYTHON_VERSION && git pull
cd $trepan_xpy_owd
rm -v */.python-version || true
