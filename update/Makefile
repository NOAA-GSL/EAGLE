ACTIVATE = . conda/etc/profile.d/conda.sh && conda activate
SRCDIRS  = eagle
TARGETS  = devenv env format lint test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

devenv:
	EAGLE_DEV=1 ./mkenv

env:
	./mkenv

format:
	@echo "=> Formatting code"
	@ruff format $(SRCDIRS)
	@echo "=> Sorting imports"
	@ruff check --select I --fix $(SRCDIRS)

lint:
	ruff check $(SRCDIRS)

test: lint typecheck unittest

typecheck:
	mypy $(SRCDIRS)

unittest:
	pytest --cov $(SRCDIRS)
