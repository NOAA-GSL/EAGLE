# EAGLE

## Quickstart: Recipe for End-to-End Run of Nested EAGLE on Ursa

In the `src/` directory:

1. Run `make env`.

This step creates the runtime software environment, comprising conda virtual environments `data`, `training`, `inference`, and `vx` for data prep, training, inference, and verification, respectively. The `conda/` subdirectory it creates is self-contained and can be removed and recreated by running `make env` again, as long as pipeline steps are not currently running.

Developers who will be modifying Python driver code should instead use `make devenv`, which will create the same environments but also install additional code-quality tools for formatting, linting, typechecking, and unit testing.
 
2. Set the `app.base` value in `eagle.yaml` to the absolute path to the current (`src/`) directory.

3. Run `make data`.

This stages data required for training and inference. The `data` target delegates to targets `grids-and-meshes`, `zarr-gfs`, and `zarr-hrrr`, which can also be run individually (e.g. `make grids-and-meshes`), but note that `grids-and-meshes`, which runs locally, must be run first. The `zarr-gfs` and `zarr-hrrr` targets can be run in quick succession, as they submit batch jobs: Do not proceed until their batch jobs complete successfully.

4. Run `make training`.

This trains a model using data staged by the previous step. It submits a batch job: Do not proceed until the batch job completes successfully.

5. Run `make inference`.

This performs inference, producing a forecast. It submits a batch job: Do not proceed until the batch job completes successfully.

6. Run `make prewxvx-global` followed by `make prewxvx-lam`.

These prepare forecast output from the previous step for verification by `wxvx`. They run locally, it is safe to proceed when the commands return.

7. Run `make` with any of the targets `vx-grid-global`, `vx-grid-lam`, `vx-obs-global`, `vs-obs-lam`.

These perform verification, either of the `global` or `lam` forecasts, and against gridded analyses (`*-grid-*`) or prepbufr observations (`*-obs-*`) as truth. Each submits a batch job, so the four `make` commands can be run in quick succession to get all the batch jobs running in parallel. When each batch job completes, MET `.stat` files and `.png` plot files can be found under the `stats/` and `plots/` subdirectories of `run/vx/grid2{grid,obs}/{global,lam}/run/`.

## Runtime Environment

To build the EAGLE runtime virtual environments:

``` bash
make env # alternatively: ./setup
```

This will install Miniforge conda in the current directory and create the virtual environments `data`, `training`, `inference`, and `vx`.

A variety of `make` targets are available to execute pipeline steps:

| Target           | Purpose                                       | Depends on target | Uses environment |
|------------------|-----------------------------------------------|-------------------|------------------|
| data             | Implies grids-and-meshes, zarr-gfs, zarr-hrrr | -                 | data             |
| grids-and-meshes | Prepare grids and meshes                      | -                 | data             |
| zarr-gfs         | Prepare Zarr-formatted GFS input data         | grids-and-meshes  | data             |
| zarr-hrrr        | Prepare Zarr-formatted HRRR input data        | grids-and-meshes  | data             |
| training         | Performs Anemoi training                      | data              | training         |
| inference        | Performs Anemoi inference                     | training          | inference        |
| prewxvx-global   | Performs postprocessing on inference          | inference         | vx               |
| prewxvx-lam      | Performs postprocessing on inference          | inference         | vx               |
| vx-grid-global   | Verify global against grided analysis         | prewxvx-global    | vx               |
| vx-grid-lam      | Verify LAM against grided analysis            | prewxvx-lam       | vx               |
| vx-obs-global    | Verify global against obs                     | prewxvx-global    | vx               |
| vx-obs-lam       | Verify LAM against obs                        | prewxvx-lam       | vx               |

Run `make` with no argument to list available targets.

## Configuration

TODO Complete this section...

The `eagle.yaml` file contains many cross-referenced values. To create the file `realized.yaml`, in which all references have been resolved to their final values, which may aid in debugging, run the command

``` bash
make realize-config
```

## Development Environment

To build the runtime virtual environments **and** install all required development packages in each environment:

``` bash
make devenv # alternatively: EAGLE_DEV=1 ./setup
```

After successful completion, the following `make` targets will be available:

``` bash
make format   # format Python code
make lint     # run the linter on Python code
make typeheck # run the typechecker on Python code
make test     # all of the above except formatting
```

## Notes

- For each `make` target that invokes an EAGLE driver, the following files will be created in the appropriate run directory:
    - `runscript.<target>`: The script to run the core component of the pipeline step. A runscripts that submits a batch job will contain batch-system directives. These scripts are self-contained and can also be manually executed (or passed to e.g. `sbatch` if they contain batch directives) to force re-execution, potentially after manual edits for debugging or experimentation purposes.
    - `runscript.<target>.out`: The captured `stdout` and `stderr` of the batch job.
    - `runscript.<target>.submit`: A file containing the job ID of the submitted batch job, if applicable.
    - `runscript.<target>.done`: Created if the core component completes successfully (i.e. exits with status code 0).
- EAGLE drivers are idempotent and, as such, will not take further action if run again unless the output they previously created is removed. In general, removing `.done` (and, when present, `.submit`) files in the appropriate run directory should suffice to reset a driver to allow it to run again, potentially overwriting its previous output. Removing or renaming the enite run directory also works.
