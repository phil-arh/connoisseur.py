import sys
import os
import shutil
import re
import argparse
from gitignore_parser import parse_gitignore
from debugprint import Debug

debug = Debug("connoisseur:modifyfilesystem")


leading_slash_re = re.compile(r"^\/")


def delete_path(path):
    """Delete a path regardless of whether a file or directory."""
    debug(f"deleting {path}")
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def copy_path(path, origin, destination):
    extension = leading_slash_re.sub("", path.replace(origin, ""))
    # debug(os.path.split(extension))
    folders = os.path.split(extension)[0]
    dest_folders = os.path.join(destination, folders)
    if not os.path.isdir(dest_folders):
        os.makedirs(dest_folders)
    shutil.copy(path, dest_folders)


def clear_empty_directories(origin):
    for root, dirs, ignored in os.walk(origin):
        for dir in dirs:
            path = os.path.join(root, dir)
            # debug(path, "path")
            # debug(os.listdir(path), "listdir")
            if not os.listdir(path):
                # debug("deleting directory")
                shutil.rmtree(path)
