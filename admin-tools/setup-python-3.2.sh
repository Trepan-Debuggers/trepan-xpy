#!/bin/bash
PYTHON_VERSION=3.2

bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi


export PATH=$HOME/.pyenv/bin/pyenv:$PATH
trepan_xpy_owd=$(pwd)
mydir=$(dirname $bs)
. $mydir/checkout_common.sh

(cd $mydir/../../../rocky && \
     setup_version python-spark python-3.2 && \
     setup_version python-xdis python-3.2 && \
     setup_version python-filecache python-3.2 && \
     cd $fulldir/../Trepan-Debugger/python3-trepan && setup_version python-3.2
)
checkout_finish python-3.2
