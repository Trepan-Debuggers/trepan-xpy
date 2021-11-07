#!/bin/bash
PACKAGE=trepanxpy

# FIXME put some of the below in a common routine
function finish {
  cd $owd
}

cd $(dirname ${BASH_SOURCE[0]})
owd=$(pwd)
trap finish EXIT

if ! source ./pyenv-versions-older ; then
    exit $?
fi
if ! source ./setup-python-3.2.sh ; then
    exit $?
fi

cd ..
source trepanxpy/version.py
echo $__version__

for pyversion in $PYVERSIONS; do
    if ! pyenv local $pyversion ; then
	exit $?
    fi
    # pip bdist_egg create too-general wheels. So
    # we narrow that by moving the generated wheel.

    # Pick out first two number of version, e.g. 3.5.1 -> 35
    first_two=$(echo $pyversion | cut -d'.' -f 1-2 | sed -e 's/\.//')
    rm -fr build
    python setup.py bdist_egg bdist_wheel
    mv -v dist/${PACKAGE}-$__version__-py3-none-any.whl dist/${PACKAGE}-$__version__-py${first_two}-none-any.whl
done
