import sys
import os
from debugprint import Debug

from .utils import printif
from . import modifyfilesystem

debug = Debug("connoisseur:tidy")


def get_files_to_tidy(origin, checker):
    output = []
    for root, dirs, files in os.walk(origin):
        for dir in dirs:
            path = os.path.join(root, dir)
            debug(path, "path")
            # debug(reject(checker, origin, path), "should reject")
            if checker.reject(path):
                output.append(path)
        for file in files:
            path = os.path.join(root, file)
            debug(path, "path")
            # debug(reject(checker, origin, path), "should reject")
            if checker.reject(path):
                output.append(path)
    return output


def tidy(origin, checker, dry_run=True, verbose=False):
    sys.stderr.write("Getting list of files to delete...\n")
    files_to_delete = get_files_to_tidy(origin, checker)
    sys.stderr.write("Deleting...")
    for path in files_to_delete:
        printif(path, (verbose or dry_run))
        if not dry_run:
            modifyfilesystem.delete_path(path)
    if not dry_run:
        modifyfilesystem.clear_empty_directories(origin)
