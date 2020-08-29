import sys
import os
import shutil
import argparse
from debugprint import Debug

from .tidy import tidy
from .copy import copy
from .checkers import CheckerFromRejectFile, CheckerFromSelectFile

debug = Debug("connoisseur:main")


def check_continue(path):
    """Perform a user check whether to continue. Exit if not confirmed."""
    should_continue = input(
        "This will probably delete or overwrite some files at {}. Are you "
        "sure you want to continue? y/N  ".format(path)
    )
    if should_continue not in "yY":
        sys.stderr.write("Not running...connoisseur will now exit.\n")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(
        prog="connoisseur", description="Utility for selective copying and deleting",
    )

    parser.add_argument(
        "action",
        choices=["copy", "tidy"],
        help="Action for connoisseur to perform - tidy up a directory tree or "
        "selectively copy it to a new one.",
    )
    parser.add_argument(
        "spec_file",
        help="Path to the spec file being used. Spec file should be written "
        "in gitignore format.",
    )
    parser.add_argument(
        "origin",
        help="Path to be tidied (in tidy) or used as a source of files to be "
        "copied to the destination (in copy).",
    )
    if len(sys.argv) > 1 and sys.argv[1] == "copy":
        parser.add_argument(
            "destination", help="Destination for files and folders to be copied to."
        )
    parser.add_argument(
        "-s",
        "--spec-type",
        choices=["select", "reject"],
        help="Set spec type - defaults to 'reject' if not specified.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="If specified, carries out a dry run - prints to stdout paths of "
        "all files to be copied (in a copy operation) or deleted (in a tidy "
        "operation) but does not alter the filesystem.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prints to stdout paths of all files copied (in a copy "
        "operation) or deleted (in a tidy operation).",
    )
    parser.add_argument(
        "-y",
        "--skip-confirmation-check",
        action="store_true",
        help="Skips confirmation check",
    )
    args = parser.parse_args()

    if args.spec_type:
        if args.spec_type == "select":
            checker = CheckerFromSelectFile(args.spec_file, args.origin)
    else:
        checker = CheckerFromRejectFile(args.spec_file, args.origin)

    if args.action == "copy":
        if os.path.isdir(args.destination) and os.listdir(args.destination):
            if not (args.skip_confirmation_check or args.dry_run):
                check_continue(args.destination)
        copy(
            args.origin,
            args.destination,
            checker,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )
    else:
        if not (args.skip_confirmation_check or args.dry_run):
            check_continue(args.origin)
        tidy(args.origin, checker, dry_run=args.dry_run, verbose=args.verbose)
