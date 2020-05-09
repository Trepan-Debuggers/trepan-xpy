# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein <rocky@gnu.org>
import os.path as osp
from typing import List, Optional

def search_file(filename: str, directories: List[str], cdir: str) -> Optional[str]:
    """Return a full pathname for filename if we can find one. path
    is a list of directories to prepend to filename. If no file is
    found we'll return None"""

    for trydir in directories:

        # Handle $cwd and $cdir
        if trydir =='$cwd': trydir='.'
        elif trydir == '$cdir': trydir = cdir

        tryfile = osp.realpath(osp.join(trydir, filename))
        if osp.isfile(tryfile):
            return tryfile
    return None

if __name__ == "__main__":
    print(search_file(__file__, ["$cwd"], "/tmp"))
