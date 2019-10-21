[![PyPi Downloads](https://pepy.tech/badge/pandas-fpl)](https://pepy.tech/project/pandas-fpl)
[![PyPi Monthly Downloads](https://pepy.tech/badge/pandas-fpl/month)](https://pepy.tech/project/pandas-fpl/month)
[![PyPi Version](https://badge.fury.io/py/pandas-fpl.svg)](https://pypi.org/project/pandas-fpl/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# Pandas wrapper for Fantasy Premier League API

The `FPLPandas` class in this package uses the [FPL](https://github.com/amosbastian/fpl) library to retrieve data from the [Fantasy Premier League API](https://fantasy.premierleague.com/api/bootstrap-static/). It maps the results to the pandas data frames so that the data can be analysed interactively, e.g. in a Jupyter notebook.

[FPL](https://github.com/amosbastian/fpl) library is an asynchronous wrapper for the [Fantasy Premier League API](https://fantasy.premierleague.com/api/bootstrap-static/) But the Jupyter notebook work better with synchronous code, the methods exposed by the `FPLPandas` class are synchronous.

## Installation

### Using pip

You can install using the pip package manager by running

    pip install pandas-fpl

### From source

Download the source code by cloning the repository or by pressing ['Download ZIP'](https://github.com/177arc/pandas-fpl/archive/master.zip) on this page.
Install by navigating to the proper directory and running

    python setup.py install

## Usage

For usage guidance, see the [Usage Jupyter Notebook](https://nbviewer.jupyter.org/github/177arc/pandas-fpl/blob/master/usage.ipynb)

## Documentation

For the code documentation, please visit the documentation [Github Pages](https://177arc.github.io/pandas-fpl/docs/fplpandas/).