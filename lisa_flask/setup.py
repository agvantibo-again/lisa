#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="lisa_flask",
    version="1.0",
    # Modules to import from other scripts:
    packages=["lisa_flask"],
    package_data={"lisa_flask": ["templates/*", "static/*"]},
)
