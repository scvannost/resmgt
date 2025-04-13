#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

from resmgt import __author__, __email__, __version__

setup(
    author=__author__,
    author_email=__email__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Simulation",
        "Typing :: Typed",
    ],
    description="resmgt.",
    install_requires=requirements,
    license="GPLv3",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="resmgt",
    packages=find_packages(),
    python_requires=">=3.9",
    test_suite="tests",
    version=__version__,
)
