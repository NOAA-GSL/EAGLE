from pathlib import Path
from typing import cast

from iotaa import Asset, collection, task
from uwtools.api.driver import DriverTimeInvariant
from uwtools.api.config import get_yaml_config


class Training(DriverTimeInvariant):
    """
    Trains an Anemoi model.
    """
    @collection
    def provisioned_rundir(self):
        yield self.taskname("provisioned run directory")
        yield [self.runscript(), self.config()]

    @task
    def config(self):
        yield self.taskname(f"training config")
        path = self.rundir / f"training.yaml"
        yield Asset(path, path.is_file)
        yield None
        get_yaml_config(self.config["anemoi"]).dump(path)

    # Public methods

    @classmethod
    def driver_name(cls) -> str:
        return "training"
