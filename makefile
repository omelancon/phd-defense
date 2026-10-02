# Builds a virtual environment with lattice-slides and all its components (matplotlib plots,
# PDF export through Playwright and Chromium). Graphviz (`dot`) is a system package: install it
# separately for dot diagrams, .dot graph files and the overview map.
#
#   make                 clone or update lattice-slides, then (re)build the venv if the sources changed
#   make lattice-slides  clone the repository, or pull the latest main if it is already there
#   make venv            rebuild the venv when what it installs changed since the last build
#   make cleanall        remove the venv, the clone and the build markers
#
# Override the defaults on the command line: make LATTICE_DIR=vendor/lattice VENV=env

LATTICE_REPO ?= git@github.com:omelancon/lattice-slides.git
LATTICE_DIR  ?= lattice-slides
VENV         ?= .venv
PYTHON       ?= python3

PIP     := $(VENV)/bin/pip
INSTALL := ./$(LATTICE_DIR)[plot,pdf]
# fingerprint of what the venv is built from (package sources, pyproject.toml, Python version
# and install spec); rewritten only when it changes
REV     := .lattice-slides.rev
STAMP   := $(VENV)/.built

.PHONY: all open lattice-slides venv clean cleanall

all: src/main.html

open: all
	open src/main.html &

src/main.html: venv $(wildcard src/*.md)
	. $(VENV)/bin/activate && lattice build src/main.md

# Always runs: clone, or fast-forward main to origin. Then records the fingerprint in $(REV),
# touching the file only when it differs so that the venv is not rebuilt for nothing. The
# fingerprint uses the git tree hashes of src/ and pyproject.toml rather than the commit, so
# commits that only touch docs, tests or examples do not trigger a rebuild.
lattice-slides:
	@if [ -d "$(LATTICE_DIR)/.git" ]; then \
	    echo "updating $(LATTICE_DIR)"; \
	    git -C "$(LATTICE_DIR)" fetch --quiet origin main && \
	    git -C "$(LATTICE_DIR)" checkout --quiet main && \
	    git -C "$(LATTICE_DIR)" merge --ff-only --quiet origin/main; \
	else \
	    git clone --branch main "$(LATTICE_REPO)" "$(LATTICE_DIR)"; \
	fi
	@{ git -C "$(LATTICE_DIR)" rev-parse HEAD:src HEAD:pyproject.toml && \
	   $(PYTHON) --version && echo "$(INSTALL)"; } > $(REV).tmp
	@if cmp -s $(REV).tmp $(REV); then rm -f $(REV).tmp; else mv -f $(REV).tmp $(REV); fi

# The venv depends only on the fingerprint. It does not depend on this Makefile: any edit to it
# (a comment, the open target) would otherwise rebuild the venv; the install spec is in $(REV).
venv: lattice-slides
	@$(MAKE) --no-print-directory $(STAMP)

$(STAMP): $(REV)
	rm -rf "$(VENV)" "$(LATTICE_DIR)/build"
	$(PYTHON) -m venv "$(VENV)"
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet "$(INSTALL)"
	$(VENV)/bin/playwright install chromium
	@command -v dot >/dev/null || echo "warning: Graphviz (dot) is not installed; dot diagrams and the overview map need it"
	@touch $@
	@echo "$$($(VENV)/bin/lattice --version) installed in $(VENV)"

clean:
	rm -rf src/main.html src/.lattice-cache

cleanall: clean
	rm -rf "$(VENV)" "$(LATTICE_DIR)" "$(REV)" "$(REV).tmp"