ACTIVATE = source conda/etc/profile.d/conda.sh && conda activate
SRCDIRS  = eagle
TARGETS  = data devenv env format grids-and-meshes lint test typecheck

.ONESHELL:

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

grids-and-meshes:
	$(ACTIVATE) data
	export FI_PSM3_UUID=eagle
	uw execute --module eagle/data.py --classname GridsAndMeshes --task run --config-file config.yaml

data: grids-and-meshes
	true

devenv:
	EAGLE_DEV=1 ./setup

env:
	./setup

format:
	./format $(SRCDIRS)

lint:
	@echo "=> Linting code"
	ruff check $(SRCDIRS)

test: lint typecheck

typecheck:
	@echo "=> Typechecking code"
	mypy $(SRCDIRS)
