PYTHON ?= .venv/bin/python
WORKERS ?= 20

.PHONY: peer-release peer-reproduce
peer-release:
	$(PYTHON) replication/release.py --workers=$(WORKERS)

peer-reproduce:
	$(PYTHON) replication/release.py --reproduce --workers=$(WORKERS)

# Conference talk: rebuild the talk figures from repository data, then the deck and script.
.PHONY: talk
talk:
	$(PYTHON) talk/figures/make_figures.py
	$(PYTHON) talk/figures/make_correspondence_figure.py
	cd talk && latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build talk.tex
	cd talk && latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build script.tex
