from build_deploy import *

log.basicConfig(level=log.INFO, format='%(message)s')

unit_test()
int_test()
build()
check()
doc()
publish(repository='pypi')