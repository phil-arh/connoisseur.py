from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="connoisseur",
    version="0.1.0",
    license="GPLv3",
    packages=find_packages(),
    author="Phil Howe",
    author_email="phil.a.r.howe@gmail.com",
    description="A utility for selective copying and deletion of complex directory structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="copy delete gitignore dockerignore docker",
    url="https://github.com/phil-arh/connoisseur.py",
)