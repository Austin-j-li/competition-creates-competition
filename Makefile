PYTHON ?= .venv/bin/python
WORKERS ?= 20

.PHONY: peer-release peer-reproduce
peer-release:
	$(PYTHON) replication/release.py --workers=$(WORKERS)

peer-reproduce:
	$(PYTHON) replication/release.py --reproduce --workers=$(WORKERS)
