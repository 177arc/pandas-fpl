import logging as log
import shutil
from shell_utils import shell

log.basicConfig(level=log.INFO, format='%(message)s')

def __execute(command: str):
    return print(shell(command, capture=True, silent=True).stdout)

def unit_test():
    log.info('Running unit tests ...')
    __execute('python -m pytest tests/unit/')

def int_test():
    log.info('Running integration tests ...')
    __execute('python -m pytest tests/integration/')

def install():
    log.info('Installing package locally ...')
    __execute('pip install .')

def build():
    log.info('Building package ...')
    shutil.rmtree('dist', ignore_errors=True)
    __execute('python setup.py sdist bdist_wheel')

def check():
    log.info('Checking package ...')
    __execute('twine check dist/*')

def doc():
    log.info('Generating documentation ...')
    __execute('pdoc --force --html --output-dir docs fplpandas')

def publish(repository='testpypi'):
    log.info(f'Publishing package to {repository} ...')
    __execute(f'twine upload --repository {repository} dist/*')