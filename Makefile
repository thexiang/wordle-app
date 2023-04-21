# in your activated python virtual env, install pyinvoke, and basic required libs
.PHONY: init
init: 
	python3 -m pip install -r requirements-local.txt -c constraints.txt