ACTIVATE = . runtime/etc/profile.d/conda.sh && conda activate
TARGETS  = build dev format lint test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

build:
	./build

dev: build
	@echo -e "=> Installing dev packages\n"
	$(ACTIVATE) && conda install -y -q -n base $(shell cat devpkgs)

format:
	@./format

lint:
	ruff check .

test: lint typecheck unittest

typecheck:
	mypy --install-types --non-interactive .

unittest:
	pytest --cov .
