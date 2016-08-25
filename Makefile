# Check if we have python3 available.
PY3_VERSION := $(shell python3 --version 2>/dev/null)
PY3_VERSION_FULL := $(wordlist 2, 4, $(subst ., , ${PY3_VERSION}))
PY3_VERSION_MAJOR := $(word 1, ${PY3_VERSION_FULL})
PY3_VERSION_MINOR := $(word 2, ${PY3_VERSION_FULL})
PY3_VERSION_PATCH := $(word 3, ${PY3_VERSION_FULL})
ifneq ($(PY3_VERSION), )
  PY_VENV := pyvenv-${PY3_VERSION_MAJOR}.${PY3_VERSION_MINOR}
  PY := $(shell which python3 2>/dev/null)
else
  PY_VENV := $(shell which virtualenv 2>/dev/null)
  PY := $(shell which python 2>/dev/null)
endif

# OK, set some globals.
WHEEL=~/wheelhouse

GIT=$(shell which git 2>/dev/null)

# Define the test suit to run.
TESTS=slagiatt/route/tests \
    slagiatt/tests

tests:
	PYTHONPATH=$(PYTHONPATH) SLAGIATT_CONF="config_for_test.py" \
	$(shell which py.test) \
	--cov-config ~/.coveragerc --cov=slagiatt -sv $(TESTS)

docs:
	PYTHONPATH=$(PYTHONPATH) $(shell which sphinx-build) \
	-b html doc/source doc/build

clean:
	$(GIT) clean -xdf

VENV_DIR_EXISTS := $(shell [ -e "venv" ] && echo 1 || echo 0)
clear_env:
ifeq ($(VENV_DIR_EXISTS), 1)
	@echo \#\#\# Deleting existing environment venv ...
	$(shell which rm) -fr venv
	@echo \#\#\# venv delete done.
endif

init_env:
ifneq ($(PY3_VERSION), )
	@echo \#\#\# Creating virtual environment venv ...
	$(PY_VENV) venv
	@echo \#\#\# venv build done.

	@echo \#\#\# Installing package dependencies ...
	venv/bin/pip install --upgrade pip
	venv/bin/pip install wheel
	venv/bin/pip install -e .
	@echo \#\#\# Package install done.
endif

init: clear_env init_env

init_env_from_wheel:
ifneq ($(PY3_VERSION), )
	@echo \#\#\# Creating virtual environment venv ...
	$(PY_VENV) venv
	@echo \#\#\# venv build done.

	@echo \#\#\# Preparing wheel environment and directory ...
	$(shell which mkdir) -pv $(WHEEL) 2>/dev/null
	venv/bin/pip install --upgrade pip
	venv/bin/pip install wheel
	@echo \#\#\# wheel env done.

	@echo \#\#\# Installing package dependencies ...
	venv/bin/pip wheel --wheel-dir $(WHEEL) --find-links=$(WHEEL) .
	venv/bin/pip install --use-wheel --find-links=$(WHEEL) -e .
	@echo \#\#\# Package install done.
endif

init_wheel: clear_env init_env_from_wheel

init_build: init_env_from_wheel build

build:
	@echo \#\#\# Building package ...
	venv/bin/python setup.py sdist bdist_wheel -d $(WHEEL)
	@echo \#\#\# Build done.

upload:
	$(PY) setup.py sdist upload -r internal

py_versions:
	@echo python3 version: ${PY3_VERSION}
	@echo path to pyvenv: ${PY_VENV}
	@echo path to python executable: ${PY}

.PHONY: tests docs py_versions init build upload
