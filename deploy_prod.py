from build_deploy import *

log.basicConfig(level=log.INFO, format='%(message)s')

unitest()
build()
check()
doc()
publish(repository='pypi')