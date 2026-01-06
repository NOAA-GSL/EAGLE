from pathlib import Path
from subprocess import check_output, STDOUT
from typing import cast

from iotaa import Asset, collection, task, log
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
        path: Path = self.rundir / f"training.yaml"
        yield Asset(path, path.is_file)
        yield None
        path.parent.mkdir(parents=True, exist_ok=True)
        output = check_output("cd %s && anemoi config generate" % self.rundir, shell=True, stderr=STDOUT)
        for line in output:
            log.info(self.taskname(line))

    # Public methods

    @classmethod
    def driver_name(cls) -> str:
        return "training"
