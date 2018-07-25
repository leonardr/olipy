#!/usr/bin/env python
import sys
from io import open
from os import walk
from os.path import join, relpath

from setuptools import setup

requires = ['textblob']

README = open('README.md', encoding='utf-8').read()

description = u'\n'.join([README])
if sys.version_info.major < 3:
    description = description.encode('utf-8')

setup(
    name='olipy',
    version='1.0',
    author='Leonard Richardson',
    author_email='leonardr@segfault.org',
    url="https://github.com/leonardr/olipy/",
    description="Python library for artistic text generation",
    license='GPLv3',
    long_description=description,
    packages=['olipy'],
    install_requires=requires,
    entry_points=entry_points,
    package_data = {
        "olipy.data": [
            "*.txt.*", 
            "*.json",
            "more-corpora/*.txt",
            "more-corpora/*.json",
            "more-corpora/README"
        ]
    }
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
