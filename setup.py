import pathlib

import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="nepse-api",
    version="0.3",
    author="Samrid Pandit",
    author_email="samrid.pandit@gmail.com",
    description="This is a API wrapper for NEPSE API.",
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
    install_requires=["aiohttp", "cachetools", "pyhumps"],
    project_urls={
        "Homepage": "https://github.com/Samrid-Pandit/nepse-api/",
    },
)
