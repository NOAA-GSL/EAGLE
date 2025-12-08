# EAGLE

## Runtime environment

To build the EAGLE runtime environment:

``` bash
make build
```

After the build completes successfully, activate the conda installation and the `workflow` environment:

``` bash
source runtime/etc/profile.d/conda.sh
conda activate workflow
```

Other virtual environments created by the build will be activated as necessary by workflow tasks.

## Development environment

To install the development code-quality tools:


``` bash
make env
```

This will create the runtime environment if it does not already exist, then install the code-quality packages into the `base` environment. In a fresh shell, run

``` bash
source runtime/etc/profile.d/conda.sh
conda activate
```

The following commands are now available:

``` bash
make format   # format Python code
make lint     # run the linter on Python code
make typeheck # run the typechecker on Python code
make unittest # run the Python unit tests
make test     # all of the above except formatting
```
