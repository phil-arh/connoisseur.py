import sys
import os
from debugprint import Debug

from .utils import printif, errif
from . import modifyfilesystem

debug = Debug("connoisseur:copy")


def get_files_to_copy(origin, destination, checker):
    output = []
    for root, ignored, files in os.walk(origin):
        for file in files:
            path = os.path.join(root, file)
            debug(path, "path")
            if checker.select(path):
                output.append(path)
    return output


def copy(origin, destination, checker, dry_run=True, verbose=False):
    sys.stdout.write("Getting list of files to copy...\n")
    files_to_copy = get_files_to_copy(origin, destination, checker)
    sys.stdout.write("Copying...\n")
    for path in files_to_copy:
        printif(path, (verbose or dry_run))
        debug("maybe copying...")
        if not dry_run:
            debug("copying...")
            modifyfilesystem.copy_path(path, origin, destination)
