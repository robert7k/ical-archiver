#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ical-archiver",
    version="0.0.1",
    author="Robert Siebeck",
    scripts=["ical-archiver.py"],
    description="Archive old entries from ICS files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robert7k/ical-archiver",
    packages=setuptools.find_packages(),
    install_requires=['icalendar>=4.0.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
