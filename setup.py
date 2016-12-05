#!/usr/bin/env python
import os
import sys
from setuptools import setup

import aiolog as pkg


def read(filename):
    with open(filename, 'rt') as f:
        return f.read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)


setup(
    name='aiolog',
    version=pkg.__version__,

    description=pkg.__doc__,
    long_description=read('README.rst'),

    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['logging', 'asyncio'],

    author='Imbolc',
    author_email='imbolc@imbolc.name',
    license='ISC',
    url='https://github.com/imbolc/aiolog',

    packages=['aiolog'],
    install_requires=['async_timeout>=1.1.0'],
)
