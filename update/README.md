# EAGLE

## Runtime Environment

To build the EAGLE runtime virtual environments:

``` bash
make env # alternatively: ./setup
```

This will install Miniforge conda in the current directory and create the virtual environments `data`, `anemoi`, and `vx`.

After the runtime virtual environments are built, activate the `base` environment:

``` bash
source conda/etc/profile.d/conda.sh
conda activate
```

Now, a variety of `make` targets are available to execute pipeline steps, each to be run with the specified environment activated:

| Target           | Purpose                                       | Depends on target | Uses environment |
|------------------|-----------------------------------------------|-------------------|------------------|
| data             | Implies grids-and-meshes, zarr-gfs, zarr-hrrr | -                 | data             |
| grids-and-meshes | Prepare grids and meshes                      | -                 | data             |
| zarr-gfs         | Prepare Zarr-formatted GFS input data         | grids-and-meshes  | data             |
| zarr-hrrr        | Prepare Zarr-formatted HRRR input data        | grids-and-meshes  | data             |
| training         | Performs Anemoi training                      | -                 | anemoi           |

Run `make` with no argument to list all available targets.

## Configuration

TODO Complete this section...

The `config.yaml` file contains many cross-referenced values. To see the fully realized configuration, in which all references have been resolved to their final values, which may aid in debugging, run the command

``` bash
make realize-config
```

## Development environment

To build the runtime virtual environments **and** install all required development packages in each environment:

``` bash
make devenv # alternatively: EAGLE_DEV=1 ./setup
```

After successful completion, the following `make` targets will be available in each environment:

``` bash
make format   # format Python code
make lint     # run the linter on Python code
make typeheck # run the typechecker on Python code
make test     # all of the above except formatting
```
