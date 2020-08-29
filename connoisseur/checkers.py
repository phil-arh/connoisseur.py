import os
from gitignore_parser import parse_gitignore
from debugprint import Debug

debug = Debug("connoisseur:checkers")


class CheckerFromRejectFile:
    def __init__(self, file_path, origin_path):
        self.origin = origin_path
        self.checker = parse_gitignore(file_path, origin_path)

    def reject(self, path):
        """Check whether a path should be rejected."""
        return self.checker(path)

    def select(self, path):
        return not self.reject(path)


class CheckerFromSelectFile:
    def __init__(self, file_path, origin_path):
        self.origin = origin_path
        negative_checker = parse_gitignore(file_path, origin_path)
        self.checker = lambda path: not negative_checker(path)

    def reject(self, path):
        """Check whether a path should be rejected."""
        return self.checker(path)

    def select(self, path):
        return not self.reject(path)
