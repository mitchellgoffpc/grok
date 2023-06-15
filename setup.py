#!/usr/bin/env python3

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(name='grok',
      version='0.1.0',
      description='grok big code real quick',
      author='Mitchell Goff',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages = ['grok'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
      ],
      install_requires=['requests', 'tqdm'],
      python_requires='>=3.8',
      extras_require={
        'linting': [
          "flake8",
          "pylint",
          "mypy",
          "pre-commit",
        ],
      },
      entry_points={
        'console_scripts': [
          'grok=grok.main:main'
        ]
      },
      include_package_data=True)
