ACTIVATE = source conda/etc/profile.d/conda.sh && conda activate
SRCDIRS  = eagle
TARGETS  = data devenv env format grids-and-meshes lint test typecheck zarr-gfs zarr-hrrr

.ONESHELL:

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

grids-and-meshes:
	$(ACTIVATE) data
	export FI_PSM3_UUID=eagle
	uw execute --module eagle/grids_and_meshes.py --classname GridsAndMeshes --task provisioned_rundir --config-file config.yaml

data:
	$(MAKE) grids-and-meshes
	$(MAKE) zarr-gfs
	$(MAKE) zarr-hrrr

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

zarr-gfs:
	$(ACTIVATE) data
	uw execute --module eagle/zarr.py --classname Zarr --task run --batch --config-file config.yaml --key-path zarrs.gfs

zarr-hrrr:
	$(ACTIVATE) data
	uw execute --module eagle/zarr.py --classname Zarr --task run --batch --config-file config.yaml --key-path zarrs.hrrr
