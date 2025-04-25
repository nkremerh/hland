CONFIG = config.json
DATA = log.json
HLAND = hland.py
LOGS = log.csv log.json

CLEAN = $(LOGS)

# Change to python3 (or other alias) if needed
PYTHON = python

# Check for local Python aliases
PYCHECK = $(shell which python > /dev/null; echo $$?)
PY3CHECK = $(shell which python3 > /dev/null; echo $$?)

all: $(DATA)

data:
	$(PYTHON) $(HLAND) --conf $(CONFIG)

setup:
	@echo "Checking for local Python installation."
ifeq ($(PY3CHECK), 0)
	@echo "Found alias for Python."
	sed -i 's/PYTHON = python$$/PYTHON = python3/g' Makefile
	sed -i 's/"python"/"python3"/g' $(CONFIG)
else ifneq ($(PYCHECK), 0)
	@echo "Could not find a local Python installation."
	@echo "Please update the Makefile and configuration file manually."
else
	@echo "This message should never be reached."
endif

clean:
	rm -rf $(CLEAN) || true

.PHONY: all clean data setup

# vim: set noexpandtab tabstop=4:
