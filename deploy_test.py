from build_deploy import *

unitest()
build()
check()
doc()
publish(repository='testpypi')