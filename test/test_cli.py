import os
import shutil
import subprocess
import pytest


def run_dir_trees_are_equal(x, y):
    for root, dirs, files in os.walk(x):
        for dir in dirs:
            assert os.path.isdir(os.path.join(root.replace(x, y), dir))
        for file in files:
            assert os.path.isfile(os.path.join(root.replace(x, y), file))


def assert_dir_trees_are_equal(x, y):
    run_dir_trees_are_equal(x, y)
    run_dir_trees_are_equal(y, x)


@pytest.fixture(autouse=True)
def run_around_tests():
    if os.path.isdir("./test/temp"):
        shutil.rmtree("./test/temp")
    # os.mkdir("./test/temp")
    yield
    # shutil.rmtree("./test/temp")
    # os.mkdir("./test/temp")


def test_tidy():
    # GIVEN
    shutil.copytree("./test/stub_input/a", "./test/temp/a")
    # WHEN
    subprocess.run(
        [
            "python",
            "-m",
            "connoisseur",
            "tidy",
            "-y",
            "-v",
            "./test/spec_files/test_tidy_reject_spec",
            "./test/temp/a",
        ]
    )
    # THEN
    assert_dir_trees_are_equal("./test/temp/a", "./test/stub_output/tidied_a")


def test_copy():
    # WHEN
    subprocess.run(
        [
            "python",
            "-m",
            "connoisseur",
            "copy",
            "-y",
            "-v",
            "./test/spec_files/test_tidy_reject_spec",
            "./test/stub_input/a",
            "./test/temp/a",
        ]
    )
    # THEN
    assert_dir_trees_are_equal("./test/temp/a", "./test/stub_output/tidied_a")


def test_dry_run_tidy():
    # GIVEN
    shutil.copytree("./test/stub_input/a", "./test/temp/a")
    # WHEN
    subprocess.run(
        [
            "python",
            "-m",
            "connoisseur",
            "tidy",
            "--dry-run",
            "./test/spec_files/test_tidy_reject_spec",
            "./test/temp/a",
        ]
    )
    subprocess.run(
        [
            "python",
            "-m",
            "connoisseur",
            "tidy",
            "-d",
            "./test/spec_files/test_tidy_reject_spec",
            "./test/temp/a",
        ]
    )
    # THEN
    assert_dir_trees_are_equal("./test/temp/a", "./test/stub_input/a")


def test_dry_run_copy():
    # GIVEN
    if os.path.isdir("./test/temp"):
        shutil.rmtree("./test/temp")
    # WHEN
    subprocess.run(
        [
            "python",
            "-m",
            "connoisseur",
            "copy",
            "--dry-run",
            "./test/spec_files/test_tidy_reject_spec",
            "./test/stub_input/a",
            "./test/temp/a",
        ]
    )
    subprocess.run(
        [
            "python",
            "-m",
            "connoisseur",
            "copy",
            "-d",
            "./test/spec_files/test_tidy_reject_spec",
            "./test/stub_input/a",
            "./test/temp/a",
        ]
    )
    # THEN
    assert not os.path.isdir("./test/temp")
