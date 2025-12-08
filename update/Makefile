ACTIVATE = . conda/etc/profile.d/conda.sh && conda activate
TARGETS  = env dev format lint test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

env:
	./env

dev: build
	@echo -e "=> Installing dev packages\n"
	$(ACTIVATE) && conda install -y -q -n workflow $(shell cat devpkgs)

format:
	@./format

lint:
	ruff check .

test: lint typecheck unittest

typecheck:
	mypy --install-types --non-interactive .

unittest:
	pytest --cov .
