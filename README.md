# Connoisseur (beta)

*A utility for selective copying and deletion of complex directory structures.*

**WARNING! This program modifies files on your file system. It is currently in beta and should be assumed to have bugs. Always do a dry run (with the `-d` flag) before running it properly and make sure you have a backup of any folders and files you run it against.**

#### A couple of example commands

```bash
connoisseur copy /path/to/spec /path/to/origin /path/to/destination

connoisseur tidy /path/to/spec /path/to/location --verbose
```

## What is it for?

Connoisseur is intended to solve a problem which I've been unable to find a decent tool for thus far - performing selective copy or deletion operations on complex directory structures.

For instance, let's say I have a folder of source code containing multiple nested git submodules, each of which contains, in addition to its own source code, test files, stub data, READMEs etc. In order to copy only the code into another directory, I would have to use a reasonably complex shell script - particularly if I also want to include additional data, e.g. UI assets.

Of course, in this particular instance you might end up using a compiler or bundler, but for certain languages and applications that would either be highly unusual (meaning high quality bundlers might not even exist) or excessively complex for the problem you need to solve.


Connoisseur solves this problem by providing utilities to selectively copy files from one location to another, and to selectively delete files in one location, using gitignore format to specify which files will be copied or deleted. No writing complex shell scripts, just write a file in gitignore syntax (something you probably already know how to do) and use the tool.

The clearest use case for this - the use case it was developed for - is in multi-stage Docker builds. Often, you might want to perform a build in one container before copying over only application files to the container that will be used for deployment. Since .dockerignore files can only be used once at the beginning of a build, there's no simple way to copy a subset of files over from the build container to the deployment container according to a complex set of rules.

## Installation

```bash
# install through pip
pip install connoisseur

# or install using Pipenv (shown here adding to dev dependencies)
pipenv --dev install connoisseur
```

## Usage

Once installed, Connoisseur can be used as a command line tool. It provides two commands - `copy` and `tidy`. More on how to use them below. First, a quick note on Connoisseur spec files.

### Connoisseur spec files

In deciding which files to copy or to delete, Connoisseur refers to a spec file, the path to which is passed to the tool as a command line argument.

Connoisseur spec files use gitignore format. If you use git, you're very likely already familiar with the format but if not [here's a quick rundown](https://git-scm.com/docs/gitignore).

#### Reject and select specs

Connoisseur can use spec files to either include or exclude paths. Spec files used to *exclude* paths are known as `reject specs` and spec files used to *include* paths are known as `select specs`.

For instance, let's say you want to copy everything apart from `test` directories and `README`s. Then you could use `connoisseur copy` with the following reject spec:

```
test
README
```

But what if you only want to copy across files ending in `.py` and `.json`? You could do this in a reject spec, but if you wanted to start using more complicated patterns it might end up becoming difficult to maintain. Instead, you're probably better off just using a select spec instead:

```
*.py
*.json
```

You can only provide one spec file at a time - either a select or a reject spec. If you don't specify what type of spec you're providing, Connoisseur will assume it's a reject spec.

**N.B. Connoisseur always assumes that you want to *keep* files specified in a select spec, and you want to *discard* files specified in a reject spec. Therefore, rejected files are `tidy`d but not `copy`d, while selected files are `copy`d but not `tidy`d.**

### Connoisseur commands

#### `copy`

`copy` copies a selection of files from one location to another, rejecting or selecting files according to the provided spec file.

The most basic way to copy using Connoisseur is as follows:

```bash
connoisseur copy /path/to/reject_spec_file /origin/path /dest/path
```

This will copy from `/origin/path` to `/dest/path` all files *not* specified by the reject spec.

If you want to use a select spec instead, you have to use the `--spec-type` or `-s` flag like:

```bash
connoisseur copy /path/to/select_spec_file /origin/path /dest/path --spec-type=select
```

This will then copy all files *that are* specified in the select file. Note that there is no syntactic difference between a select and reject spec file - the only way for Connoisseur to know that it's being passed a select spec is for it to be specified with the `--spec-type` argument.

#### `tidy`

`tidy` clears a directory of unwanted files and folders, deleting rejected files and keeping selected files according to the provided spec file.

A basic tidy command is:

```bash
connoisseur tidy /path/to/reject_spec_file /path/to/be/tidied
```

As with `copy`, you can specify that the spec file is to be treated as a select file with the `--spec-type` flag:

```bash
connoisseur tidy /path/to/select_spec_file /path/to/be/tidied --spec-type=select
```

#### Additional command line options

##### `--verbose` or `-v`

Running with this flag prints to terminal all files *copied* in a `connoisseur copy` operation or all files *deleted* in a `connoisseur tidy` operation.

##### `--dry-run` or `-d`

Performs the same print-out as `--verbose` but doesn't perform the operation - so no filesystem operations actually take place. As a result, also skips the confirmation check.

##### `--skip-confirmation-check` or `-y`

Skips the confirmation prompt that normally shows when using Connoisseur. Useful in CI pipelines and Docker builds.

## Recursion limit

If you're trying to use Connoisseur on very deeply nested directory structures, you may hit your system recursion limit. On most systems, this is 1000 stack frames, which in the context of Connoisseur means a maximum directory depth of 998. If this happens, you can look at raising Python's recursion limit (provided you've got enough memory to handle that). To do that, you'll need to import Connoisseur to a Python script and call the script as a command line tool like:

```python
# in a file called extra_recursion_connoisseur.py
import sys
import connoisseur

sys.setrecursionlimit(1500) # or however high it needs to be
connoisseur.main()

# call this script at command line like: python3 extra_recursion_connoisseur.py copy /path/to/reject_spec ...etc.
```

Beware though! At some point, your system will become unstable if the recursion limit is too high as Connoisseur might end up using excessive amounts of memory.

I'll probably see at some point if I can re-implement directory walking iteratively but until then this is probably your best bet to deal with very deep directory nesting.

## Testing

Test using pytest by doing `pytest test`. To get debug printout run `DEBUG=connoisseur pytest -s test`.
