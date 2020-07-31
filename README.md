[![PyPi Downloads](https://pepy.tech/badge/pandas-fpl)](https://pepy.tech/project/pandas-fpl)
[![PyPi Monthly Downloads](https://pepy.tech/badge/pandas-fpl/month)](https://pepy.tech/project/pandas-fpl/month)
[![PyPi Version](https://badge.fury.io/py/pandas-fpl.svg)](https://pypi.org/project/pandas-fpl/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/177arc/pandas-fpl/master?filepath=usage.ipynb)

# Pandas wrapper for Fantasy Premier League API

The `FPLPandas` class in this package uses the excellent [FPL](https://github.com/amosbastian/fpl) library to retrieve data from the [Fantasy Premier League API](https://fantasy.premierleague.com/api/bootstrap-static/). It maps the results to the pandas data frames so that the data can be analysed interactively, e.g. in a Jupyter notebook.

[FPL](https://github.com/amosbastian/fpl) library is an asynchronous wrapper for the [Fantasy Premier League API](https://fantasy.premierleague.com/api/bootstrap-static/) But the Jupyter notebook work better with synchronous code, the methods exposed by the `FPLPandas` class are synchronous.

## Installation

### Using pip

You can install using the pip package manager by running

    pip install pandas-fpl

### From source

Download the source code by cloning the repository or by pressing [Download ZIP](https://github.com/177arc/pandas-fpl/archive/master.zip) on this page.
Install by navigating to the proper directory and running

    python setup.py install

## Usage

For usage guidance and testing the package interactively, hit the [Usage Jupyter Notebook](https://mybinder.org/v2/gh/177arc/pandas-fpl/master?filepath=usage.ipynb).

## Documentation

For the code documentation, please visit the [Documentation Github Pages](https://177arc.github.io/pandas-fpl/docs/fplpandas/).

## Contributing

1. Fork the repository on GitHub.
2. Run the tests with `python -m pytest tests/` to confirm they all pass on your system.
   If the tests fail, then try and find out why this is happening. If you aren't
   able to do this yourself, then don't hesitate to either create an issue on
   GitHub, contact me on Discord or send an email to [py@177arc.net](mailto:py@177arc.net>).
3. Either create your feature and then write tests for it, or do this the other
   way around.
4. Run all tests again with with `python -m pytest tests/` to confirm that everything
   still passes, including your newly added test(s).
5. Create a pull request for the main repository's ``master`` branch.