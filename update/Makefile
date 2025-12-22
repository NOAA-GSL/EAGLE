SRCDIRS  = eagle
TARGETS  = data devenv env format grids-and-meshes lint test typecheck zarr-gfs zarr-hrrr

activate = source conda/etc/profile.d/conda.sh && conda activate $(1)
exec     = uw execute --config-file config.yaml --module eagle/$(1).py --classname $(2) --task $(3)
zarr     = $(call exec,zarr,Zarr,run --batch --key-path zarrs.$(1))

.ONESHELL:
.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

grids-and-meshes:
	export FI_PSM3_UUID=eagle
	$(call activate,data)
	$(call exec,grids_and_meshes,GridsAndMeshes,provisioned_rundir)

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
	$(call activate, data)
	$(call zarr,gfs)

zarr-hrrr:
	$(call activate, data)
	$(call zarr,hrrr)
