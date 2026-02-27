ENVS    = data inference training vx
HELPERS = prewxvx vx zarr
PACKAGE = eagle
STEPS   = data grids-and-meshes inference prewxvx-global prewxvx-lam training vx-grid-global vx-grid-lam vx-obs-global vx-obs-lam zarr-gfs zarr-hrrr
TOOLING = devenv env format lint test typecheck

activate = source conda/etc/profile.d/conda.sh && conda activate $(1)
checkcfg = @$(if $(config),,$(error config= argument required))
envloop  = @for env in $(ENVS); do $(MAKE) --no-print-directory env=$$env $(1); done
exec     = uw execute --config-file $(config) --module $(PACKAGE)/$(1)/$(2).py --classname $(3) --task $(4)
tasklist = uw execute --module $(PACKAGE)/$(1)/$(2).py --classname $(3)

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
	$(call activate,data)
ifeq ($(task),?)
	$(call tasklist,data,grids_and_meshes,GridsAndMeshes)
else
	$(call exec,data,grids_and_meshes,GridsAndMeshes,$(or $(task),provisioned_rundir))
endif

inference:
	$(call checkcfg)
	$(call activate,inference)
ifeq ($(task),?)
	$(call tasklist,inference,inference,Inference)
else
	$(call exec,inference,inference,Inference,$(or $(task),run) --batch)
endif

lint:
ifdef env
	@echo "=> Linting package: $$env"
	$(call activate,$(env))
	ruff check $(PACKAGE)/$(env)
else
	$(call envloop,lint)
endif

prewxvx:
	$(call checkcfg) # PM FIXME take argument, also check extent=
	$(call activate,vx)
ifeq ($(task),?)
	$(call tasklist,vx,prewxvx,PreWXVX)
else
	$(call exec,vx,prewxvx,PreWXVX,$(or $(task),run) --key-path prewxvx.$(extent))
endif

prewxvx-global:
	$(MAKE) prewxvx extent=global

prewxvx-lam:
	$(MAKE) prewxvx extent=lam

test: lint typecheck

training:
	$(call checkcfg)
	$(call activate,training)
ifeq ($(task),?)
	$(call tasklist,training,training,Training)
else
	$(call exec,training,training,Training,$(or $(task),run) --batch)
endif

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
ifeq ($(task),?)
	$(call tasklist,vx,vx,VX)
else
	$(call exec,vx,vx,VX,$(or $(task),run) --key-path vx.$(truth).$(extent) --batch)
endif

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
ifeq ($(task),?)
	$(call tasklist,data,zarr,Zarr)
else
	$(call exec,data,zarr,Zarr,$(or $(task),run) --key-path zarrs.$(source) --batch)
endif

zarr-gfs:
	$(MAKE) zarr source=gfs

zarr-hrrr:
	$(MAKE) zarr source=hrrr
