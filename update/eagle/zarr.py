from pathlib import Path
from typing import cast

import yaml
from iotaa import Asset, collection, task
from uwtools.api.driver import DriverTimeInvariant


class Zarr(DriverTimeInvariant):
    @collection
    def provisioned_rundir(self):
        yield self.taskname("provisioned run directory")
        yield [self.runscript(), self.ufs2arco_config()]

    @task
    def ufs2arco_config(self):
        yield self.taskname(f"ufs2arco {self.name} config")
        path = self.rundir / f"ufs2arco-{self.name}.yaml"
        yield Asset(path, path.is_file)
        yield None
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            yaml.dump(self.config["ufs2arco"], f)

    # Public methods

    @classmethod
    def driver_name(cls) -> str:
        return "zarr"

    @property
    def name(self) -> str:
        return cast("str", self.config["name"])

    # Private methods

    @property
    def _runscript_path(self) -> Path:
        return self.rundir / f"runscript.{self.driver_name()}-{self.name}"
