#!/bin/bash
PYTHON_VERSION=3.7.7

owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi
mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..
(cd ../python-spark && git checkout master && pyenv local $PYTHON_VERSION) && git pull && \
    (cd ../python-xdis && git checkout master && pyenv local $PYTHON_VERSION) && \
    (cd ../python3-trepan && git checkout master && pyenv local $PYTHON_VERSION) && git pull && \
    git checkout master &&  pyenv local $PYTHON_VERSION && git pull
cd $owd
rm -v */.python-version || true
