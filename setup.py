import pathlib

import setuptools

from nepse import (
    __author__,
    __author_email__,
    __package_description__,
    __package_name__,
    __version__,
)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__package_description__,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">3.7",
    keywords="api-wrapper stock",
    install_requires=["cachetools", "pyhumps", "httpx"],
    project_urls={
        "Homepage": "https://github.com/Samrid-Pandit/nepse-api/",
    },
)
