SRCDIRS  = eagle
TARGETS  = data devenv env format lint test typecheck

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

data:
	uw execute --module eagle/data.py --classname Data --task provisioned_rundir --config-file config.yaml

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

test: lint typecheck

typecheck:
	mypy $(SRCDIRS)
