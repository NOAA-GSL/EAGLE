# EAGLE

This repository contains configuration and driver code for running an end-to-end machine learning pipeline for weather prediction. The pipeline is orchestrated with `make` targets and `uwtools`-based drivers, and it provisions a self-contained set of conda environments to support each step of the workflow. A typical run follows these steps:

- **Environment setup:** Creates the runtime environments used by each stage of the pipeline.
- **Prepare training and inference data:** Provisions required static assets (e.g., grids and meshes) and produces Zarr-formatted datasets via `ufs2arco`.
- **Train an AI model:** Trains an Anemoi model using the provisioned datasets, producing checkpoints for inference.
- **Generate a forecast:** Runs inference from training checkpoints using `anemoi-inference` to produce forecast output.
- **Prepare output for verification:** Postprocesses forecast output into the formats and directory structure expected by `wxvx`.
- **Verify model performance:** Runs `wxvx` verification against gridded analysis and/or observations, producing MET statistics and plots.

## Quickstart: Recipe for End-to-End Run of Nested EAGLE on Ursa

In the `src/` directory:

### 1. Run `make env`.

This step creates the runtime software environment, comprising conda virtual environments `data`, `training`, `inference`, and `vx` for data prep, training, inference, and verification, respectively. The `conda/` subdirectory it creates is self-contained and can be removed and recreated by running `make env` again, as long as pipeline steps are not currently running.

Developers who will be modifying Python driver code should instead use `make devenv`, which will create the same environments but also install additional code-quality tools for formatting, linting, typechecking, and unit testing.
 
### 2. Set the `app.base` value in `eagle.yaml` to the absolute path to the current (`src/`) directory.

The run directories from subsequent steps, along with the output of those steps, will be created in the `run/` subdirectory of `app.base`.

### 3. Run `make config=eagle.yaml data`.

This step provisions data required for training and inference. The `data` target delegates to targets `grids-and-meshes`, `zarr-gfs`, and `zarr-hrrr`, which can also be run individually (e.g. `make grids-and-meshes`), but note that `grids-and-meshes`, which runs locally, must be run first. The `zarr-gfs` and `zarr-hrrr` targets can be run in quick succession, as they submit batch jobs: Do not proceed until their batch jobs complete successfully (see the files `run/data/*.out`).

### 4. Run `make config=eagle.yaml training`.

This step trains a model using data provisioned by the previous step. It submits a batch job: Do not proceed until the batch job completes successfully (see the file `run/training/runscript.training.out`).

### 5. Run `make config=eagle.yaml inference`.

This step performs inference, producing a forecast. It submits a batch job: Do not proceed until the batch job completes successfully (see the file `run/inference/runscript.inference.out`.)

### 6. Run `make config=eagle.yaml prewxvx-global` followed by `make config=eagle.yaml prewxvx-lam`.

These steps prepare forecast output from the previous step for verification by `wxvx`. They run locally, it is safe to proceed when the commands return. See the files `run/vx/prewxvx/{global,lam}/runscript.prewxvx-*.out` for details.

### 7. Run `make config=eagle.yaml` followed by any of the targets `vx-grid-global`, `vx-grid-lam`, `vx-obs-global`, `vs-obs-lam`.

These steps perform verification, either of the `global` or `lam` forecasts, and against gridded analyses (`*-grid-*`) or prepbufr observations (`*-obs-*`) as truth. Each submits a batch job, so the four `make` commands can be run in quick succession to get all the batch jobs running in parallel. When each batch job completes, MET `.stat` files and `.png` plot files can be found under the `stats/` and `plots/` subdirectories of `run/vx/grid2{grid,obs}/{global,lam}/run/`. The files `run/vx/*.log` contain the logs from each verification run.

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
| prewxvx-global   | Postprocesses global inference output         | inference         | vx               |
| prewxvx-lam      | Postprocesses LAM inference output            | inference         | vx               |
| vx-grid-global   | Verify global against grided analysis         | prewxvx-global    | vx               |
| vx-grid-lam      | Verify LAM against grided analysis            | prewxvx-lam       | vx               |
| vx-obs-global    | Verify global against obs                     | prewxvx-global    | vx               |
| vx-obs-lam       | Verify LAM against obs                        | prewxvx-lam       | vx               |

Run `make` with no argument to list available targets.

## Configuration

The following subsections describe various parts of the EAGLE YAML config.

Some configuration parameters are common across `uwtools`-based component drivers and occur in multiple configuration blocks:

- The [execution:](https://uwtools.readthedocs.io/en/stable/sections/user_guide/yaml/components/execution.html) block provides information required to correctly execute the component.
- The [platform:](https://uwtools.readthedocs.io/en/stable/sections/user_guide/yaml/components/platform.html) block provides information about the system EAGLE is running on.
- The `rundir:` parameter specifies where driver runtime assets will be created.

Additionally, many configuration blocks include a `common:` block, which provides parameters shared by several configurations, to avoid unnecessary repetition.

### app

This block provides various global configuration parameters for the application, especially those thought most likely to require configuration by users.

### grids_and_meshes

Configuration for the `GridsAndMeshes` driver.

- The `filenames:` block provides paths to data files created by this step.

### inference

Configuration for the `Inference` driver.

- The `anemoi:` block provides the YAML config for the [anemoi-inference](https://anemoi.readthedocs.io/projects/inference/en/latest/index.html#) component.
- The `checkpoint_dir:` parameter specifies the location of the checkpoints created by the training step.

### platform

In the EAGLE base config, this `uwtools`-required parameter delegates to `app.platform`.

### prewxvx

Configuration for the `PreWXVX` driver.

- This driver executes the [eagle-tools](https://pypi.org/project/eagle-tools/) component.
- The `global:` and `lam:` blocks provide configurations for global and limited-area extents, respectively, each borrowing from `common:`. Their `prewxvx:` sub-blocks are ultimately passed to the `PreWXVX` driver as its runtime configuration.

### training

Configuration for the `Training` driver.

- The `anemoi:` block provides the YAML config for the [anemoi-training](https://anemoi.readthedocs.io/projects/training/en/latest/index.html#) component.
- The `remove:` block specifies values from the default configurations [generated by Anemoi](https://anemoi.readthedocs.io/projects/training/en/stable/start/hydra-intro.html#generating-user-config-files) that should be removed at execution time, via the [override syntax](https://hydra.cc/docs/advanced/override_grammar/basic/#basic-override-syntax) of [Hydra](https://hydra.cc/), the YAML-processing tool used by Anemoi.

### ufs2arco

This block provides general configuration parameters for the [ufs2arco](https://ufs2arco.readthedocs.io/en/latest/) component. This configuration is used as a source for default/common configuration parameters, which are supplemented by the `Zarr` driver then it executes `ufs2arco` for specific use cases.

### val

This block provides both static and derived values that are referenced by other configuration blocks. It is the appropriate place to define values that need to be shared and kept in-sync across pipeline steps, but less likely to be manually modified by users like values in the `app:` block.

### vx

Configuration for the `VX` driver.

- This driver executes the [wxvx](https://github.com/NOAA-GSL/wxvx) component.
- The `grid2grid:` block provides configuration for running `wxvx` with MET's [grid_stat](https://metplus.readthedocs.io/projects/met/en/latest/Users_Guide/grid-stat.html) tool to verify against gridded analyses. Sub-blocks `global:` and `lam:` provide configuration refinements for verifying global and limited-area grids, respectively.
- The `grid2obs:` block provides configuration for running `wxvx` with MET's [point_stat](https://metplus.readthedocs.io/projects/met/en/develop/Users_Guide/point-stat.html) tool to verify against point observations. Sub-blocks `global:` and `lam:` provide configuration refinements for verifying global and limited-area grids, respectively.

### zarrs

Configuration for the `Zarr` driver.

- This driver executes the [ufs2arco](https://ufs2arco.readthedocs.io/en/latest/) component.
- The `gfs:` and `hrrr:` sub-blocks provide refinements for ingesting GFS and HRRR data, respectively, for EAGLE.

## Development

### Environment

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

The `lint` and `typecheck` targets accept an optional `env=<name>` key-value pair that, if provided, will restrict the tool to the code associated with a particular virtual environment. For example, `make env=data lint` will lint only the code associated with the `data` environment. If no `env` value is provided, all code will be tested.

## Notes

- For each `make` target that executes an EAGLE driver, the following files will be created in the appropriate run directory:
    - `runscript.<target>`: The script to run the core component of the pipeline step. A runscripts that submits a batch job will contain batch-system directives. These scripts are self-contained and can also be manually executed (or passed to e.g. `sbatch` if they contain batch directives) to force re-execution, potentially after manual edits for debugging or experimentation purposes.
    - `runscript.<target>.out`: The captured `stdout` and `stderr` of the batch job.
    - `runscript.<target>.submit`: A file containing the job ID of the submitted batch job, if applicable.
    - `runscript.<target>.done`: Created if the core component completes successfully (i.e. exits with status code 0).
- EAGLE drivers are idempotent and, as such, will not take further action if run again unless the output they previously created is removed. In general, removing `.done` (and, when present, `.submit`) files in the appropriate run directory should suffice to reset a driver to allow it to run again, potentially overwriting its previous output. Removing or renaming the enite run directory also works.

## Further Reading 

For more information about model configurations, please see our [documentation](https://epic-eagle.readthedocs.io/en/latest/). 

## Acknowledgments

ufs2arco: Tim Smith (NOAA Physical Sciences Laboratory)
- [Github](https://github.com/NOAA-PSL/ufs2arco)
- [Documentation](https://ufs2arco.readthedocs.io/en/latest/)

Anemoi: European Centre for Medium-Range Weather Forecasts
- [anemoi-core github](https://github.com/ecmwf/anemoi-core)
- [anemoi-inference github](https://github.com/ecmwf/anemoi-inference)
- Documentation: [anemoi-models](https://anemoi.readthedocs.io/projects/models/en/latest/index.html), [anemoi-graphs](https://anemoi.readthedocs.io/projects/graphs/en/latest/), [anemoi-training](https://anemoi.readthedocs.io/projects/training/en/latest/), [anemoi-inference](https://anemoi.readthedocs.io/projects/inference/en/latest/)

wxvx: Paul Madden (NOAA Global Systems Laboratory/Cooperative Institute for Research In Environmental Sciences)
- [Github](https://github.com/maddenp-cu/wxvx)

eagle-tools: Tim Smith (NOAA Physical Sciences Laboratory)
- [Github](https://github.com/NOAA-PSL/eagle-tools)
