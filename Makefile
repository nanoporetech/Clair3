
PYTHON ?= python3
VENV=venv

venv: ${VENV}/bin/activate
IN_VENV=. ./${VENV}/bin/activate

$(VENV)/bin/activate:
	test -d $(VENV) || $(PYTHON) -m venv $(VENV) --prompt "clair3"
	${IN_VENV} && pip install --upgrade pip setuptools


.PHONY: develop
develop: venv
	${IN_VENV} && python setup.py develop


