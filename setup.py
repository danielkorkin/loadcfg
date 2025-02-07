#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# Read the long description from README.md (if available)
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "loadcfg: A configuration helper library for JSON and YAML config files."

setup(
    name="loadcfg",
    version="0.1.0",
    description="A configuration helper library for JSON and YAML config files with dot-access.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Korkin",
    author_email="daniel.d.korkin@gmail.com",
    url="https://github.com/danielkorkin/loadcfg",
    project_urls={
        "Documentation": "https://loadcfg.readthedocs.io",
        "Code Coverage": "https://app.codecov.io/gh/danielkorkin/loadcfg/",
        "PyPI": "https://pypi.org/project/loadcfg",
        "Source": "https://github.com/danielkorkin/loadcfg",
    },
    packages=find_packages(),  # Automatically find packages in the directory.
    install_requires=[
        "PyYAML>=5.1",  # Required for YAML file support.
        "toml>=0.10.2",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pre-commit",
            "black",
            "isort",
            "ruff",
            "yamllint",
            "pytest-cov",
            "codecov",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    python_requires=">=3.6",
)
