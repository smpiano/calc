#!/usr/bin/env python

"""
Setup script for calc
"""
from setuptools import find_packages
from setuptools import setup

DEPENDENCIES=[
    "tk"
]

setup(
    author="smpiano",
    author_email="smpiano@gmail.com",
    description="Test calculator",
    install_requires=DEPENDENCIES,
    name='calc',
    packages=find_packages(exclude=['test*.*', 'tests']),
    version='0.0.1'
)
