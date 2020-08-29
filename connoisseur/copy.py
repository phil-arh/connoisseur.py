import sys
import os
from debugprint import Debug

from .utils import printif, errif
from . import modifyfilesystem

debug = Debug("connoisseur:copy")


def _get_files_to_copy(origin, checker):
    output = []
    for item in map(lambda x: os.path.join(origin, x), os.listdir(origin)):
        if checker.select(item):
            if os.path.isfile(item):
                output.append(item)
            else:
                output.extend(_get_files_to_copy(item, checker))
    return output


def copy(origin, destination, checker, dry_run=True, verbose=False):
    sys.stderr.write("Getting list of files to copy...\n")
    files_to_copy = _get_files_to_copy(origin, checker)
    sys.stderr.write("Copying...\n")
    for path in files_to_copy:
        printif(path, (verbose or dry_run))
        debug("maybe copying...")
        if not dry_run:
            debug("copying...")
            modifyfilesystem.copy_path(path, origin, destination)
