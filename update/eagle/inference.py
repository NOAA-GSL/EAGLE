from pathlib import Path
from subprocess import run

from iotaa import Asset, collection, task
from uwtools.api.config import get_yaml_config
from uwtools.api.driver import DriverTimeInvariant


class Inference(DriverTimeInvariant):
    """
    Runs Anemoi inference.
    """

    # Public tasks

    @task
    def anemoi_config(self):
        yield self.taskname("inference config")
        path = self.rundir / "inference.yaml"
        yield Asset(path, path.is_file)
        yield None
        path.parent.mkdir(parents=True, exist_ok=True)
        #if inference is a top-level key it might not need to specified.
        config = get_yaml_config(config=self.config["inference"])
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
        return "inference"