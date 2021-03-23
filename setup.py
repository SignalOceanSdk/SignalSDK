from setuptools import setup, find_packages
from os import path
import re


def read_file(file_name: str) -> str:
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, file_name), encoding="utf-8") as f:
        return f.read()


long_description = read_file("README.md")
version = re.sub("\s+", "", read_file("version.txt"))

setup(
    name="signal-ocean",
    version=version,
    description="Access Signal Ocean Platform data using Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Signal Ocean Developers",
    author_email="signaloceandevelopers@thesignalgroup.com",
    license="Apache 2.0",
    url="https://apis.signalocean.com/",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.23.0,<3",
        "python-dateutil>=2.8.1,<3",
        "pandas>=1.0.3,<2",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
    ],
    project_urls={
        "The Signal Group": "https://www.thesignalgroup.com/",
        "Signal Ocean": "https://www.signalocean.com/",
        "The Signal Ocean Platform": "https://app.signalocean.com",
    },
)
