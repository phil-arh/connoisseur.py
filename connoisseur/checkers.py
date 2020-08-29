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
