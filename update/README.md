# EAGLE

# EAGLE Runtime Build

To build the EAGLE runtime environment:

``` bash
make build
```

After the build completes successfully, activate the workflow virtual environment:

``` bash
source runtime/etc/profile.d/conda.sh
conda activate workflow
```

Other virtual environments created by the build will be activated as necessary by workflow tasks.
