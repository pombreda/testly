#!/usr/bin/env python

import os
from setuptools import setup

setup(
    name='Testly',
    version='0.1',
    url='https://github.com/lavelle/testly',

    author='Giles Lavelle',
    author_email='giles.lavelle@gmail.com',

    description='Test a program\'s basic IO using JSON test cases',
    long_description=open(os.path.join(os.path.dirname(__file__), 'readme.md')).read(),

    install_requires=[
        'watchdog',
        'pystache'
    ],
    py_modules=['testly']
)
