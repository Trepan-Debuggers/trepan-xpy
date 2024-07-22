#/bin/bash
cd $(dirname ${BASH_SOURCE[0]})
if . ./setup-python-2.7.sh; then
    git merge python-3.2-to-3.5
fi
