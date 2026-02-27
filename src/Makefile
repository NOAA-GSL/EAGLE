ENVS    = data inference training vx
HELPERS = prewxvx vx zarr
PACKAGE = eagle
STEPS   = data grids-and-meshes inference prewxvx-global prewxvx-lam training vx-grid-global vx-grid-lam vx-obs-global vx-obs-lam zarr-gfs zarr-hrrr
TOOLING = devenv env format lint test typecheck

activate = @source conda/etc/profile.d/conda.sh && conda activate $(1)
check    = @$(if $(1),,$(error $(2)= argument required))
envloop  = @for env in $(ENVS); do $(make) env=$$env $(1); done
exec     = set -x && uw execute --config-file $(config) --module $(PACKAGE)/$(1)/$(2).py --classname $(3) --task $(4)
make     = $(MAKE) --no-print-directory
tasklist = @(set -x && uw execute --module $(PACKAGE)/$(1)/$(2).py --classname $(3)) || true

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
	$(make) grids-and-meshes
	$(make) zarr-gfs
	$(make) zarr-hrrr

devenv:
	EAGLE_DEV=1 ./setup

env:
	./setup

format:
	$(call activate,base)
	./format $(PACKAGE)

grids-and-meshes:
	$(call activate,data)
ifeq ($(task),?)
	$(call tasklist,data,grids_and_meshes,GridsAndMeshes)
else
	$(call check,$(config),config)
	$(call exec,data,grids_and_meshes,GridsAndMeshes,$(or $(task),provisioned_rundir))
endif

inference:
	$(call activate,inference)
ifeq ($(task),?)
	$(call tasklist,inference,inference,Inference)
else
	$(call check,$(config),config)
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
	$(call activate,vx)
ifeq ($(task),?)
	$(call tasklist,vx,prewxvx,PreWXVX)
else
	$(call check,$(config),config)
	$(call check,$(extent),extent)
	$(call exec,vx,prewxvx,PreWXVX,$(or $(task),run) --key-path prewxvx.$(extent))
endif

prewxvx-global:
	$(make) prewxvx extent=global

prewxvx-lam:
	$(make) prewxvx extent=lam

test: lint typecheck

training:
	$(call activate,training)
ifeq ($(task),?)
	$(call tasklist,training,training,Training)
else
	$(call check,$(config),config)
	$(call exec,training,training,Training,$(or $(task),run) --batch)
endif

typecheck:
ifdef env
	@echo "=> Typechecking package: $$env"
	$(call activate,$(env))
	mypy $(PACKAGE)/$(env)
else
	$(call envloop,typecheck)
endif

vx:
	$(call activate,vx)
ifeq ($(task),?)
	$(call tasklist,vx,vx,VX)
else
	$(call check,$(config),config)
	$(call check,$(extent),extent)
	$(call check,$(truth),truth)
	$(call exec,vx,vx,VX,$(or $(task),run) --key-path vx.$(truth).$(extent) --batch)
endif

vx-grid-global:
	$(make) vx truth=grid2grid extent=global

vx-grid-lam:
	$(make) vx truth=grid2grid extent=lam

vx-obs-global:
	$(make) vx truth=grid2obs extent=global

vx-obs-lam:
	$(make) vx truth=grid2obs extent=lam

zarr:
	$(call activate,data)
ifeq ($(task),?)
	$(call tasklist,data,zarr,Zarr)
else
	$(call check,$(config),config)
	$(call check,$(source),source)
	$(call exec,data,zarr,Zarr,$(or $(task),run) --key-path zarrs.$(source) --batch)
endif

zarr-gfs:
	$(make) zarr source=gfs

zarr-hrrr:
	$(make) zarr source=hrrr
