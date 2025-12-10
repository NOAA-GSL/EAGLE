ACTIVATE = source conda/etc/profile.d/conda.sh && conda activate
SRCDIRS  = eagle
TARGETS  = devenv env format grids_and_meshes lint test typecheck

.ONESHELL:

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

grids_and_meshes:
	$(ACTIVATE) grids_and_meshes
	export FI_PSM3_UUID=eagle
	uw execute --module eagle/grids_and_meshes.py --classname GridsAndMeshes --task grids_and_meshes --config-file config.yaml

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
