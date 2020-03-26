"""A setuptools based setup module."""
from os import path
from setuptools import setup, find_packages
from io import open


setup(
    name='Flask Blueprint api',
    version='0.0.1',
    description='Search browser',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Flask',
    packages=find_packages(),
    install_requires=['Flask',
                      'python-dotenv'],

)
