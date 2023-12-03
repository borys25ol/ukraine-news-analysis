Ukraine News Analysis
====================

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat)](https://github.com/pre-commit/pre-commit)

Analysis of 3 Ukraine news sources (only Volyn resources):
- bug.org.ua
- insider-media.net
- volynnews.com


Developing
-----------

Install pre-commit hooks to ensure code quality checks and style checks

    $ make install_hooks


You can also use these commands during dev process:

- To run mypy checks

      $ make types

- To run flake8 checks

      $ make style

- To run black checks:

      $ make format

- To run together:

      $ make lint

Local install
-------------

Setup and activate a python3 virtualenv via your preferred method. e.g. and install production requirements:

    $ make ve

For remove virtualenv:

    $ make clean


Local run
-------------
Run Jupyter Notebook with code analysis:

    $ cd analysis
    $ make run_jupyter

Run local scrapers to get datasets:
  
    $ scrapy crawl bug.org.ua -o datasets/bug.csv 
    $ scrapy crawl volynnews.com -o datasets/volynnews.csv 
    $ scrapy crawl insider-media.net -o datasets/insider_media.csv 
