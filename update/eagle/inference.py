from pathlib import Path

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
        config = get_yaml_config(self.config["anemoi"])
        ckpt_dir = Path(self._config["checkpoint_dir"])
        ckpts = sorted(ckpt_dir.glob("*/inference-last.ckpt"))
        config["checkpoint_path"] = str(ckpts[-1])
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
