SRCDIRS  = eagle
REALIZED = realized.yaml
TARGETS  = data devenv env format grids-and-meshes inference lint prewxvx-global prewxvx-lam realize-config test training typecheck vx-grid-global vx-grid-lam vx-obs-global vx-obs-lam zarr-gfs zarr-hrrr

activate = source conda/etc/profile.d/conda.sh && conda activate $(1)
exec     = uw execute --config-file eagle.yaml --module eagle/$(1).py --classname $(2) --task $(3)
prewxvx  = $(call exec,prewxvx,PreWXVX,run --key-path prewxvx.$(1))
wxvx     = $(call exec,vx,VX,run --key-path vx.$(1).$(2) --batch)
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
	$(call activate,inference)
	$(call exec,inference,Inference,run --batch)

lint:
	@echo "=> Linting code"
	$(call activate,data)
	ruff check $(SRCDIRS)

prewxvx-global:
	$(call activate,vx)
	$(call prewxvx,global)

prewxvx-lam:
	$(call activate,vx)
	$(call prewxvx,lam)

realize-config: $(REALIZED)

test: lint typecheck

training:
	$(call activate,training)
	$(call exec,training,Training,run --batch)

typecheck:
	$(call activate,data)
	@echo "=> Typechecking code"
	mypy $(SRCDIRS)

vx-grid-global:
	$(call activate,vx)
	$(call wxvx,grid2grid,global)

vx-grid-lam:
	$(call activate,vx)
	$(call wxvx,grid2grid,lam)

vx-obs-global:
	$(call activate,vx)
	$(call wxvx,grid2obs,global)

vx-obs-lam:
	$(call activate,vx)
	$(call wxvx,grid2obs,lam)

zarr-gfs:
	$(call activate,data)
	$(call zarr,gfs)

zarr-hrrr:
	$(call activate,data)
	$(call zarr,hrrr)

$(REALIZED): eagle.yaml
	$(call activate,base)
	uw config realize --input-file $< --output-file $@
