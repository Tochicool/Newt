# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Newt',
    version='0.0.1',
    description='Physics Simulator',
    long_description=readme,
    author='Tochukwu Obudulu',
    author_email='tochicool@gmail.com',
    url='https://github.com/tochicool',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

