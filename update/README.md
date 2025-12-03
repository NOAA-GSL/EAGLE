# EAGLE

# EAGLE Runtime Build

To build the EAGLE runtime environment, `cd` to an appropriate directory and execute the `build` script accompanying this document to create an `eagle/` directory:

``` bash
/path/to/build
```

After the build completes successfully, activate the workflow virtual environment:

``` bash
source eagle/etc/profile.d/conda.sh
conda activate workflow
```

Other virtual environments created by the build will be activated as necessary by workflow tasks.
