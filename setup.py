import setuptools

from nepse import (
    __author__,
    __author_email__,
    __package_description__,
    __package_name__,
    __version__,
)

setuptools.setup(
    name="nepse-api",
    ame=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__package_description__,
)

"""
WARNING: DON'T USE THIS FOR INSTALLATION OR DEPLOYMENT
======================================================

USE POETRY FOR INSTALLATION OF THE PACKAGE INSTEAD
==================================================

INFO
----
This file was only created so that github will
recognize this as the official repo for `nepse-api`
PyPi module.
"""
