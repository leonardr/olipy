#!/usr/bin/env python
import sys
from io import open

import setuptools

requires = ['textblob', 'wordfilter', 'internetarchive', 'requests']

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='olipy',
    version='1.0.3',
    author='Leonard Richardson',
    author_email='leonardr@segfault.org',
    url="https://github.com/leonardr/olipy/",
    description="Python library for artistic text generation",
    license='GPLv3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'olipy.apollo = olipy.example:apollo',
            'olipy.board_games = olipy.example:board_games',
            'olipy.corrupt = olipy.example:corrupt',
            'olipy.dinosaurs = olipy.example:dinosaurs',
            'olipy.ebooks = olipy.example:ebooks',
            'olipy.gibberish = olipy.example:gibberish',
            'olipy.mashteroids = olipy.example:mashteroids',
            'olipy.sonnet = olipy.example:sonnet',
            'olipy.typewriter = olipy.example:typewriter',
            'olipy.words = olipy.example:words',
        ]
    },
    package_data = {
        "olipy": [
            "data/%s/*.json" % ("*/" * x)
            for x in range(10)
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Text Processing',
        'Topic :: Artistic Software',
    ],
)
