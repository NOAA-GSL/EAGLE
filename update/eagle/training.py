from pathlib import Path
from subprocess import STDOUT, run
from typing import cast

from iotaa import Asset, collection, log, task
from uwtools.api.config import get_yaml_config
from uwtools.api.driver import DriverTimeInvariant


class Training(DriverTimeInvariant):
    """
    Trains an Anemoi model.
    """

    @task
    def anemoi_config(self):
        yield self.taskname(f"training config")
        path = self.rundir / f"training.yaml"
        yield Asset(path, path.is_file)
        yield None
        path.parent.mkdir(parents=True, exist_ok=True)
        logfile = self.rundir / "config.log"
        run("anemoi-training config generate >%s 2>&1" % logfile, cwd=self.rundir, shell=True)
        config = get_yaml_config(self.rundir / "config.yaml")
        config.update_from(self.config["anemoi"])
        config.dump(path)

    @collection
    def provisioned_rundir(self):
        yield self.taskname("provisioned run directory")
        yield [
            self.anemoi_config(),
            self.runscript(),
        ]

    # Public methods

    @classmethod
    def driver_name(cls) -> str:
        return "training"
