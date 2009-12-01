"""
Autoexec script to repeat a given test command whenever .py files change.
"""

import os
import time
from stat import ST_SIZE, ST_MTIME
from fabric.api import *


def autoexec(command=None, sleep=1):
    """
    Autoexec a given command whenever a file changes.

    It considers the fabfile.py directory as the project root directory, then
    monitors changes in any inner python files.

    Usage:

        fab autoexec:"manage.py test -v 0"
        fab autoexec:"manage.py test myapp.TestSomeCase"

    This is based on Jeff Winkler's nosy script.
    """

    def checkSum():
        '''
        Return a long which can be used to know if any .py files have changed.
        Looks in all project's subdirectory.
        '''

        def hash_stat(file):
            stats = os.stat(file)
            return stats[ST_SIZE] + stats[ST_MTIME]

        hash_ = 0
        for root, dirs, files in os.walk(os.path.dirname(__file__)):
            # We are only interested int python files
            files = [os.path.join(root, f) for f in files if f.endswith('.py')]
            hash_ += sum(map(hash_stat, files))
        return hash_

    if command is None:
        raise ValueError("Test command expected.")

    val = 0
    while(True):
        new_val = checkSum()
        if val != new_val:
            val = new_val
            os.system(command)
        time.sleep(sleep)
