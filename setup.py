#!/usr/bin/env python

"""
Setup script for calc
"""
from setuptools import find_packages
from setuptools import setup

package = __import__('src')

DEPENDENCIES=[
    "tk"
]

setup(
    author=package.__author__,
    author_email=package.__email__,
    description=package.__doc__.strip(),
    install_requires=DEPENDENCIES,
    name='calc',
    url=package.__source__,
    packages=find_packages(exclude=['test*.*', 'tests']),
    version=package.__version__
)
