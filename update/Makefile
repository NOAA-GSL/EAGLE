SRCDIRS  = eagle
REALIZED = realized.yaml
TARGETS  = data devenv env format grids-and-meshes inference lint realize-config test training typecheck zarr-gfs zarr-hrrr

activate = source conda/etc/profile.d/conda.sh && conda activate $(1)
exec     = uw execute --config-file nested_eagle.yaml --module eagle/$(1).py --classname $(2) --task $(3)
zarr     = $(call exec,zarr,Zarr,run --key-path zarrs.$(1) --batch)

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
	$(call activate,data)
	./format $(SRCDIRS)

inference:
	$(call activate,anemoi)
	$(call exec,inference,Inference,run --batch)

lint:
	@echo "=> Linting code"
	$(call activate,anemoi)
	ruff check $(SRCDIRS)

realize-config: $(REALIZED)

test: lint typecheck

training:
	$(call activate,anemoi)
	$(call exec,training,Training,run --batch)

typecheck:
	$(call activate,data)
	@echo "=> Typechecking code"
	mypy $(SRCDIRS)

zarr-gfs:
	$(call activate,data)
	$(call zarr,gfs)

zarr-hrrr:
	$(call activate,data)
	$(call zarr,hrrr)

$(REALIZED): nested_eagle.yaml
	$(call activate,base)
	uw config realize --input-file $< --output-file $@
