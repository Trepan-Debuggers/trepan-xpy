#!/bin/bash
PYTHON_VERSION=3.6

trepan_xpy_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi


mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/../../../rocky

(cd ./python-spark && ./admin-tools/setup-master.sh && pyenv local $PYTHON_VERSION && git pull)
(cd ../python3-trepan && ./admin-tools/setup-python-3.6.sh)
(cd ../Trepan-Debuggers/python3-trepan && git checkout master && pyenv local $PYTHON_VERSION && git pull)
(cd $fulldir/.. && git checkout python-3.6-to-3.10 && pyenv local $PYTHON_VERSION && git pull)
set +x
cd $trepan_xpy_owd
rm -v */.python-version || true
