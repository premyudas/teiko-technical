.PHONY: setup pipeline dashboard clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

pipeline:
	$(PYTHON) load_data.py

dashboard:
	$(PYTHON) app.py

clean:
	rm -f cell_counts.db
	rm -rf $(VENV)