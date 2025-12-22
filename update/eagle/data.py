import yaml
from iotaa import Asset, collection, task
from uwtools.api.driver import DriverTimeInvariant


class ZarrDataset(DriverTimeInvariant):
    # Public tasks

    @collection
    def provisioned_rundir(self):
        yield self.taskname("provisioned run directory")
        yield [
            *[self._ufs2arco_config(x) for x in self.config["ufs2arco"]],
            self.runscript(),
        ]

    # Private tasks

    @task
    def _ufs2arco_config(self, name: str):
        yield self.taskname(f"ufs2arco {name} config")
        path = self.rundir / f"ufs2arco-{name}.yaml"
        yield Asset(path, path.is_file)
        yield None
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            yaml.dump(self.config["ufs2arco"][name], f)

    # Public methods

    @classmethod
    def driver_name(cls) -> str:
        return "zarr-dataset"
