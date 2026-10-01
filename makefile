# Builds a virtual environment with lattice-slides and all its components (matplotlib plots,
# PDF export through Playwright and Chromium). Graphviz (`dot`) is a system package: install it
# separately for dot diagrams, .dot graph files and the overview map.
#
#   make                 clone or update lattice-slides, then (re)build the venv if the sources changed
#   make lattice-slides  clone the repository, or pull the latest main if it is already there
#   make venv            rebuild the venv when the checked-out commit changed since the last build
#   make cleanall        remove the venv, the clone and the build markers
#
# Override the defaults on the command line: make LATTICE_DIR=vendor/lattice VENV=env

LATTICE_REPO ?= git@github.com:omelancon/lattice-slides.git
LATTICE_DIR  ?= lattice-slides
VENV         ?= .venv
PYTHON       ?= python3

PIP   := $(VENV)/bin/pip
# the commit the venv was built from; rewritten only when it changes
REV   := .lattice-slides.rev
STAMP := $(VENV)/.built

.PHONY: all lattice-slides venv clean cleanall

all: src/talk.html

src/talk.html: venv
	. $(VENV)/bin/activate && lattice build src/talk.md

# Always runs: clone, or fast-forward main to origin. Then records the checked-out commit in
# $(REV), touching the file only when the commit differs so that the venv is not rebuilt for nothing.
lattice-slides:
	@if [ -d "$(LATTICE_DIR)/.git" ]; then \
	    echo "updating $(LATTICE_DIR)"; \
	    git -C "$(LATTICE_DIR)" fetch --quiet origin main && \
	    git -C "$(LATTICE_DIR)" checkout --quiet main && \
	    git -C "$(LATTICE_DIR)" merge --ff-only --quiet origin/main; \
	else \
	    git clone --branch main "$(LATTICE_REPO)" "$(LATTICE_DIR)"; \
	fi
	@rev=$$(git -C "$(LATTICE_DIR)" rev-parse HEAD); \
	if [ "$$rev" != "$$(cat $(REV) 2>/dev/null)" ]; then echo "$$rev" > $(REV); fi

# The venv depends on the recorded commit (and on this Makefile, whose install line defines it).
venv: lattice-slides
	@$(MAKE) --no-print-directory $(STAMP)

$(STAMP): $(REV) $(firstword $(MAKEFILE_LIST))
	rm -rf "$(VENV)"
	$(PYTHON) -m venv "$(VENV)"
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet "./$(LATTICE_DIR)[plot,pdf]"
	$(VENV)/bin/playwright install chromium
	@command -v dot >/dev/null || echo "warning: Graphviz (dot) is not installed; dot diagrams and the overview map need it"
	@touch $@
	@echo "$$($(VENV)/bin/lattice --version) installed in $(VENV)"

clean:
	rm -rf src/talk.html .lattice-cache

cleanall: clean
	rm -rf "$(VENV)" "$(LATTICE_DIR)" "$(REV)"