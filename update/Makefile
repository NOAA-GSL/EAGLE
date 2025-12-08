ACTIVATE = . conda/etc/profile.d/conda.sh && conda activate
TARGETS  = build devenv format lint test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

build:
	./build

dev: env
	$(ACTIVATE) && mamba install -y -n base $(shell cat devpkgs)

format:
	@./format

lint:
	ruff check .

test: lint typecheck unittest

typecheck:
	mypy --install-types --non-interactive .

unittest:
	pytest --cov .
