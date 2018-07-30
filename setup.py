#!/usr/bin/env python
import sys
from io import open
from os import walk
from os.path import join, relpath

import setuptools

requires = ['textblob', 'wordfilter']

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='olipy',
    version='1.0.0',
    author='Leonard Richardson',
    author_email='leonardr@segfault.org',
    url="https://github.com/leonardr/olipy/",
    description="Python library for artistic text generation",
    license='GPLv3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requires,
    package_data = {
        "olipy.data": [
            "olipy/data/*/*.json",
        ]
    }
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Text Processing',
        'Topic :: Artistic Software',
    ],
)
