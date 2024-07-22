#/bin/bash
cd $(dirname ${BASH_SOURCE[0]})
if . ./setup-python-3.2.sh; then
    git merge master
fi
