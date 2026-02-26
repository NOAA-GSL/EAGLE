ENVS    = data inference training vx
HELPERS = prewxvx vx zarr
PACKAGE = eagle
STEPS   = data grids-and-meshes inference prewxvx-global prewxvx-lam training vx-grid-global vx-grid-lam vx-obs-global vx-obs-lam zarr-gfs zarr-hrrr
TOOLING = devenv env format lint test typecheck

activate = source conda/etc/profile.d/conda.sh && conda activate $(1)
checkcfg = @$(if $(config),,$(error config= argument required))
envloop   = @for env in $(ENVS); do $(MAKE) --no-print-directory env=$$env $(1); done
exec     = uw execute --config-file $(config) --module $(PACKAGE)/$(1)/$(2).py --classname $(3) --task $(4)
prewxvx  = $(call exec,vx,prewxvx,PreWXVX,run --key-path prewxvx.$(1))
wxvx     = $(call exec,vx,vx,VX,run --key-path vx.$(1).$(2) --batch)
zarr     = $(call exec,data,zarr,Zarr,run --key-path zarrs.$(1) --batch)

.ONESHELL:
.PHONY: $(HELPERS) $(STEPS) $(TOOLING)

all:
	@echo Available targets:
	@echo
	@echo Pipeline steps: $(STEPS)
	@echo Tooling: $(TOOLING)
	@echo
	false

data:
	$(MAKE) grids-and-meshes
	$(MAKE) zarr-gfs
	$(MAKE) zarr-hrrr

devenv:
	EAGLE_DEV=1 ./setup

env:
	./setup

format:
	$(call activate,base)
	./format $(PACKAGE)

grids-and-meshes:
	$(call checkcfg)
	export FI_PSM3_UUID=eagle
	$(call activate,data)
	$(call exec,data,grids_and_meshes,GridsAndMeshes,provisioned_rundir)

inference:
	$(call checkcfg)
	$(call activate,inference)
	$(call exec,inference,inference,Inference,run --batch)

lint:
ifdef env
	@echo "=> Linting package: $$env"
	$(call activate,$(env))
	ruff check $(PACKAGE)/$(env)
else
	$(call envloop,lint)
endif

prewxvx:
	$(call checkcfg)
	$(call activate,vx)
	$(call prewxvx,$(extent))

prewxvx-global:
	$(MAKE) prewxvx extent=global

prewxvx-lam:
	$(MAKE) prewxvx extent=lam

test: lint typecheck

training:
	$(call checkcfg)
	$(call activate,training)
	$(call exec,training,training,Training,run --batch)

typecheck:
ifdef env
	@echo "=> Typechecking package: $$env"
	$(call activate,$(env))
	mypy $(PACKAGE)/$(env)
else
	$(call envloop,lint)
endif

vx:
	$(call checkcfg)
	$(call activate,vx)
	$(call wxvx,$(truth),$(extent))

vx-grid-global:
	$(MAKE) vx truth=grid2grid extent=global

vx-grid-lam:
	$(MAKE) vx truth=grid2grid extent=lam

vx-obs-global:
	$(MAKE) vx truth=grid2obs extent=global

vx-obs-lam:
	$(MAKE) vx truth=grid2obs extent=lam

zarr:
	$(call checkcfg)
	$(call activate,data)
	$(call zarr,$(source))

zarr-gfs:
	$(MAKE) zarr source=gfs

zarr-hrrr:
	$(MAKE) zarr source=hrrr
