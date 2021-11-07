<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Get latest sources:](#get-latest-sources)
- [Change version in trepanxpy/version.py.](#change-version-in-trepanxpyversionpy)
- [Update ChangeLog:](#update-changelog)
- [Update NEWS.md from ChangeLog. Then:](#update-newsmd-from-changelog-then)
- [Switch to python-3.2, sync that up and build that first since it creates a tarball which we don't want.](#switch-to-python-32-sync-that-up-and-build-that-first-since-it-creates-a-tarball-which-we-dont-want)
- [Make packages and check](#make-packages-and-check)
- [Check package on github](#check-package-on-github)
- [Release on Github](#release-on-github)
- [Get on PyPI](#get-on-pypi)
- [Move dist files to uploaded](#move-dist-files-to-uploaded)

<!-- markdown-toc end -->

# Get latest sources:

    $ git pull

# Change version in trepanxpy/version.py.

    $ emacs trepanxpy/version.py
    $ source trepanxpy/version.py
    $ echo $__version__
    $ git commit -m"Get ready for release $__version__" .


# Update ChangeLog:

    $ make ChangeLog

#  Update NEWS.md from ChangeLog. Then:

    $ emacs NEWS.md
    $ remake -c check
    $ git commit --amend .
    $ git push   # get CI testing going early

# Switch to python-3.2, sync that up and build that first since it creates a tarball which we don't want.

    $ source admin-tools/setup-python-3.2.sh
    $ git merge master

# Make packages and check

    $ make dist-older
	$ pyenv local 3.8.3
	$ twine check dist/trepanxpy-$__version__*
    $ git tag release-python-3.2-$__version__
    $ make dist-newer
	$ twine check dist/trepanxpy-$__version__*

# Check package on github

Todo: turn this into a script in `admin-tools`

	$ mkdir /tmp/gittest; pushd /tmp/gittest
	$ pyenv local 3.7.5
	$ pip install -e git://github.com/rocky/trepan-xpy.git#egg=trepanxpy
	$ trepan-xpy -V # see that new version appears
	$ trepan-xpy src/trepanxpy/test/example/gcd.py 3 5
	$ pip uninstall trepanxpy
	$ popd

# Release on Github

Goto https://github.com/rocky/trepan-xpy/releases/new

Get version from `$__version__`. Copy from `NEWS.md`
Upload eggs, wheels, and tarball

Now check the tagged release.

Todo: turn this into a script in `admin-tools`

    $ git pull # to pull down new tag
    $ pushd /tmp/gittest
	$ pyenv local 3.7.5
	$ pip install -e git://github.com/rocky/trepan-xpy.git@${VERSION}#egg=trepanxpy
	$ trepan-xpy -V # see that new version appears
	$ pip uninstall trepanxpy
	$ popd

Now check the tagged release.

Todo: turn this into a script in `admin-tools`

    $ git pull # to pull down new tag
    $ pushd /tmp/gittest
	$ pyenv local 3.7.5
	$ pip install -e git://github.com/rocky/trepan-xpy.git@${VERSION}#egg=trepanxpy
	$ trepan-xpy -V # see that new version appears
	$ trepan-xpy src/trepanxpy/test/example/gcd.py 3 5
	$ pip uninstall trepanxpy
	$ popd

# Get on PyPI

	$ twine upload dist/trepanxpy-${VERSION}*

Check on https://pypi.org/project/trepan-xpy/

# Move dist files to uploaded

	$ mv -v dist/trepanxpy-${VERSION}* dist/uploaded
