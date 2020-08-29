import sys
import os
from debugprint import Debug

from .utils import printif
from . import modifyfilesystem

debug = Debug("connoisseur:tidy")


def _get_files_to_tidy(origin, checker):
    output = []
    for item in map(lambda x: os.path.join(origin, x), os.listdir(origin)):
        if checker.reject(item):
            output.append(item)
        elif os.path.isdir(item):
            output.extend(_get_files_to_tidy(item, checker))
    return output


def tidy(origin, checker, dry_run=True, verbose=False):
    sys.stderr.write("Getting list of files to delete...\n")
    files_to_delete = _get_files_to_tidy(origin, checker)
    sys.stderr.write("Deleting...")
    for path in files_to_delete:
        printif(path, (verbose or dry_run))
        if not dry_run:
            modifyfilesystem.delete_path(path)
    if not dry_run:
        modifyfilesystem.clear_empty_directories(origin)
