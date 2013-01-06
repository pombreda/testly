#!/usr/bin/env python

# from distutils.core import setup
import os
from setuptools import setup, find_packages

setup(
    name='Testly',
    version='0.1',
    url='https://github.com/lavelle/testly',

    author='Giles Lavelle',
    author_email='giles.lavelle@gmail.com',

    description='Test a program\'s basic IO using JSON test cases',
    long_description=open(os.path.join(os.path.dirname(__file__), 'readme.md')).read(),

    py_modules=['testly']
)
