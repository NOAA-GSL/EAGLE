# EAGLE

## Runtime Environment

To build the EAGLE runtime virtual environments:

``` bash
make env # alternatively: ./mkenv
```

After the build completes successfully, activate the conda installation and the `base` environment:

``` bash
source conda/etc/profile.d/conda.sh
conda activate
```

Other virtual environments will be activated as necessary by pipeline steps.

## Development environment

To install the runtime virtual environments, complete with all required development packagesin each environment:

``` bash
make devenv # alternatively: EAGLE_DEV=1 ./mkenv
```

After successful completion, the following `make` targets will be available in each environment:

``` bash
make format   # format Python code
make lint     # run the linter on Python code
make typeheck # run the typechecker on Python code
make unittest # run the Python unit tests
make test     # all of the above except formatting
```
