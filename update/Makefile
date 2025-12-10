ACTIVATE = source conda/etc/profile.d/conda.sh && conda activate
SRCDIRS  = eagle
TARGETS  = devenv env format data lint test typecheck

.ONESHELL:

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

data:
	$(ACTIVATE) data
	export FI_PSM3_UUID=eagle
	uw execute --module eagle/data.py --classname Data --task run --config-file config.yaml

devenv:
	EAGLE_DEV=1 ./setup

env:
	./setup

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
