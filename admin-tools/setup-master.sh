#!/bin/bash
PYTHON_VERSION=3.13

trepan_xpy_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
trepan_xpy_fulldir=$(readlink -f $mydir)
. $trepan_xpy_fulldir/checkout_common.sh

(
     cd $trepan_xpy_fulldir/../../../rocky && setup_version x-python master && \
     cd $trepan_xpy_fulldir/../.. && setup_version python3-trepan master
)
checkout_finish master
