#!/bin/bash
PYTHON_VERSION=3.6

trepan_xpy_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
trepan_xpy_fulldir=$(readlink -f $mydir)
. $mydir/checkout_common.sh

(
     cd $trepan_xpy_fulldir/../../../rocky && setup_version x-python python-3.6 && \
     cd $trepan_xpy_fulldir/../.. && setup_version python3-trepan python-3.6
)
checkout_finish python-3.6-to-3.10
