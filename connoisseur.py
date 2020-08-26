import sys
import os
import shutil
import re
import argparse
from gitignore_parser import parse_gitignore
from debugprint import Debug

debug = Debug("connoisseur")

leading_slash_re = re.compile(r"^\/")


def errpr(string, should_print):
    if should_print:
        sys.stderr.write("{}\n".format(string))


def printif(string, should_print):
    if should_print:
        print(string)


def check_continue(path):
    return
    """
    should_continue = input(
        "This will probably delete or overwrite some files at {}. Are you "
        "sure you want to continue? y/N  ".format(path)
    )
    if should_continue not in "yY":
        print("Not running...connoisseur will now exit.")
        sys.exit()
    """


def get_absolute_path(relative_path):
    """Convert a relative path to an absolute path."""
    return os.path.join(os.getcwd(), relative_path)


def delete_path(path):
    """Delete a path regardless of whether a file or directory."""
    debug(f"deleting {path}")
    """
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
    """


def copy_path(path, origin, destination):
    extension = leading_slash_re.sub("", path.replace(origin, ""))
    # debug(os.path.split(extension))
    folders = os.path.split(extension)[0]
    dest_folders = os.path.join(destination, folders)
    if not os.path.isdir(dest_folders):
        os.makedirs(dest_folders)
    shutil.copy(path, dest_folders)


class CheckerFromRejectFile:
    def __init__(self, file_path, origin_path):
        self.origin = origin_path
        self.checker = parse_gitignore(file_path, origin_path)

    def reject(self, path):
        """Check whether a path should be rejected."""
        extension = path.replace(self.origin, "").split("/")
        full_path = self.origin
        for item in extension:
            full_path = os.path.join(full_path, item)
            debug(full_path, "full_path")
            debug(self.checker(full_path), "should reject")
            if self.checker(full_path):
                return True
        return False

    def select(self, path):
        return not self.reject(path)


class CheckerFromSelectFile:
    def __init__(self, file_path, origin_path):
        self.origin = origin_path
        negative_checker = parse_gitignore(file_path, origin_path)
        self.checker = lambda path: not negative_checker(path)

    def reject(self, path):
        """Check whether a path should be rejected."""
        extension = path.replace(self.origin, "").split("/")
        full_path = self.origin
        for item in extension:
            full_path = os.path.join(full_path, item)
            debug(full_path, "full_path")
            debug(self.checker(full_path), "should reject")
            if not self.checker(full_path):
                return False
        return True

    def select(self, path):
        return not self.reject(path)


def get_files_to_copy(origin, destination, checker):
    output = []
    if not os.path.isdir(destination):
        os.makedirs(destination)
    for root, ignored, files in os.walk(origin):
        for file in files:
            path = os.path.join(root, file)
            debug(path, "path")
            if checker.select(path):
                output.append(path)
    return output


def copy(origin, destination, checker, dry_run=False, verbose=False):
    errpr("Getting list of files to copy...", (verbose or dry_run))
    files_to_copy = get_files_to_copy(origin, destination, checker)
    errpr("Copying...", (verbose or dry_run))
    for path in files_to_copy:
        printif(path, (verbose or dry_run))
        if not dry_run:
            copy_path(path, origin, destination)


def clear_empty_directories(origin):
    for root, dirs, ignored in os.walk(origin):
        for dir in dirs:
            path = os.path.join(root, dir)
            if not os.listdir(path):
                shutil.rmtree(path)


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


def tidy(origin, checker, dry_run=False, verbose=False):
    errpr("Getting list of files to delete...", (dry_run or verbose))
    files_to_delete = get_files_to_tidy(origin, checker)
    errpr("Deleting...", (dry_run or verbose))
    for path in files_to_delete:
        printif(path, (verbose or dry_run))
        if not dry_run:
            delete_path(path)
    clear_empty_directories(origin)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="connoisseur", description="Utility for selective copying and deleting",
    )

    parser.add_argument("action")
    parser.add_argument("connoisseur_file")
    parser.add_argument("origin", type=str)
    if sys.argv[1] == "copy":
        parser.add_argument(
            "destination", type=str,
        )
    parser.add_argument("-s", "--spec-type", choices=["select", "reject"])
    parser.add_argument("-d", "--dry-run", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # debug(dir(args))
    if args.file_type:
        if args.file_type == "select":
            checker = CheckerFromSelectFile(args.connoisseur_file, args.origin)
    else:
        checker = CheckerFromRejectFile(args.connoisseur_file, args.origin)

    if args.action == "copy":
        if os.path.isdir(args.destination) and os.listdir(args.destination):
            check_continue(args.destination)
        copy(
            args.origin,
            args.destination,
            checker,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )
    else:
        check_continue(args.origin)
        tidy(args.origin, checker, dry_run=args.dry_run, verbose=args.verbose)
