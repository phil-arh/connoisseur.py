import sys


def errif(string, should_print):
    if should_print:
        sys.stderr.write("{}\n".format(string))


def printif(string, should_print):
    if should_print:
        print(string)


def check_maximum_recursion(fn):
    def recursion_safe_fn(*args):
        try:
            return fn(*args)
        except RecursionError:
            sys.stderr.write(
                "Error: maximum recursion depth exceeded. You are probably "
                "attempting to copy or tidy a very deeply nested directory "
                "tree (hundreds or thousands of directories deep). "
                "Unfortunately, the current implementation of Connoisseur "
                "isn't able to handle directories nested to that level as "
                "Python doesn't support tail-call recursion.\nConnoisseur "
                "will now exit.\n",
            )
