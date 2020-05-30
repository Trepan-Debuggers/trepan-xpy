<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Get latest sources:](#get-latest-sources)
- [Change version in trepanxpy/version.py.](#change-version-in-trepanxpyversionpy)
- [Update ChangeLog:](#update-changelog)
- [Update NEWS.md from ChangeLog. Then:](#update-newsmd-from-changelog-then)
- [Update NEWS.md from master branch](#update-newsmd-from-master-branch)
- [Make packages and check](#make-packages-and-check)
- [Get on PyPy](#get-on-pypy)

<!-- markdown-toc end -->

# Get latest sources:

    $ git pull

# Change version in trepanxpy/version.py.

    $ emacs trepanxpy/version.py
    $ source trepanxpy/version.py
    $ echo $VERSION
    $ git commit -m"Get ready for release $VERSION" .


# Update ChangeLog:

    $ make ChangeLog

#  Update NEWS.md from ChangeLog. Then:

    $ emacs NEWS.md
    $ remake -c check
    $ git commit --amend .
    $ git push   # get CI testing going early

# Update NEWS.md from master branch

    $ git commit -m"Get ready for release $VERSION" .

# Make packages and check

    $ ./admin-tools/make-dist.sh
	$ twine check dist/trepanxpy-$VERSION*

# Get on PyPy

Goto https://github.com/rocky/trepan-xpy/releases/new


	$ twine upload dist/trepanxpy-${VERSION}-py37-none-any.whl  # Older versions don't support Markdown
	$ twine upload dist/trepanxpy-${VERSION}*

Check on https://pypi.org/project/trepan-xpy/

# Move dist files to uploaded

	$ mv -v dist/trepan-xpy-${VERSION}* dist/uploaded
