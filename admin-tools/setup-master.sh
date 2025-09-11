#!/bin/bash
PYTHON_VERSION=3.11

trepan_xpy_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/../../../rocky


(cd ./python-spark && git checkout master && pyenv local $PYTHON_VERSION && git pull)
(cd ./python-xdis ; git checkout master && pyenv local $PYTHON_VERSION && git pull)
pwd
(cd ../Trepan-Debuggers/python3-trepan && git checkout master && pyenv local $PYTHON_VERSION && git pull)
(cd $trepay_xpy_owd/.. && git checkout master &&  pyenv local $PYTHON_VERSION && git pull)
cd $trepan_xpy_owd
rm -v */.python-version || true
