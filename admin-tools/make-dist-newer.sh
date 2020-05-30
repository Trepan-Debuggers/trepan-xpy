#!/bin/bash
PACKAGE=trepan-xpy
PACKAGE2=trepan-xpy

# FIXME put some of the below in a common routine
function finish {
  cd $owd
}

cd $(dirname ${BASH_SOURCE[0]})
owd=$(pwd)
trap finish EXIT

if ! source ./pyenv-versions-newer ; then
    exit $?
fi
if ! source ./setup-master.sh ; then
    exit $?
fi

cd ..
source trepanxpy/version.py
echo $VERSION

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
<<<<<<< HEAD
    mv -v dist/${PACKAGE}-$VERSION-py3-none-any.whl dist/${PACKAGE}-$VERSION-py${first_two}-none-any.whl
=======
    mv -v dist/${PACKAGE}-$VERSION-py3-non-any.whl dist/${PACKAGE2}-$VERSION-py$first_two}-none-any.whl
>>>>>>> e8ae17e7665bbf08357b9397c690b8754054ff0a
done

python ./setup.py sdist
