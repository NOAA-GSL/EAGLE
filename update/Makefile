SRCDIRS  = eagle
REALIZED = realized.yaml
TARGETS  = data devenv env format grids-and-meshes inference lint prewxvx realize-config test training typecheck vx zarr-gfs zarr-hrrr

activate = source conda/etc/profile.d/conda.sh && conda activate $(1)
exec     = uw execute --config-file eagle.yaml --module eagle/$(1).py --classname $(2) --task $(3)
prewxvx  = $(call exec,prewxvx,PreWXVX,run --key-path prewxvx.$(1) --batch)
wxvx     = $(call exec,vx,WXVX,run --key-path vx.$(1).$(2) --batch)
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

grid2grid-global:
	$(call activate,vx)
	$(call wxvx,grid2grid,global)

grid2grid-lam:
	$(call activate,vx)
	$(call wxvx,grid2grid,lam)

grid2obs-global:
	$(call activate,vx)
	$(call wxvx,grid2obs,global)

grid2obs-lam:
	$(call activate,vx)
	$(call wxvx,grid2obs,lam)

inference:
	$(call activate,anemoi)
	$(call exec,inference,Inference,run --batch)

lint:
	@echo "=> Linting code"
	$(call activate,anemoi)
	ruff check $(SRCDIRS)

prewxvx:
	$(MAKE) prewxvx-global
	$(MAKE) prewxvx-lam

prewxvx-global:
	$(call activate,vx)
	$(call prewxvx,global)

prewxvx-lam:
	$(call activate,vx)
	$(call prewxvx,lam)

realize-config: $(REALIZED)

test: lint typecheck

training:
	$(call activate,anemoi)
	$(call exec,training,Training,run --batch)

typecheck:
	$(call activate,data)
	@echo "=> Typechecking code"
	mypy $(SRCDIRS)

vx:
	$(MAKE) prewxvx
	$(MAKE) grid2grid-global
	$(MAKE) grid2grid-lam
	$(MAKE) grid2obs-global
	$(MAKE) grid2obs-lam

zarr-gfs:
	$(call activate,data)
	$(call zarr,gfs)

zarr-hrrr:
	$(call activate,data)
	$(call zarr,hrrr)

$(REALIZED): eagle.yaml
	$(call activate,base)
	uw config realize --input-file $< --output-file $@
