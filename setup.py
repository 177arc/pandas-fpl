import pathlib
from setuptools import setup

# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
readme = (cwd / 'README.md').read_text()

# This call to setup() does all the work
setup(name='pandas-fpl',
        version='0.3.0',
        description='Pandas wrapper for Fantasy Premier League API based on the FPL package: https://github.com/amosbastian/fpl',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/177arc/pandas-fpl',
        author='Marc Maier',
        author_email='py@177arc.net',
        license='MIT',
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        packages=['fplpandas'],
        include_package_data=True,
        install_requires=['pandas', 'fpl']
)