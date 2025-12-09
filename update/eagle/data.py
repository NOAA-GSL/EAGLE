from pathlib import Path
import cf_xarray as cfxr
import numpy as np
import xesmf
from anemoi.datasets.grids import cutout_mask
from anemoi.graphs.generate.utils import get_coordinates_ordering
from ufs2arco import sources
from iotaa import Asset, collection, task
from uwtools.api.driver import AssetsTimeInvariant


class EAGLEData(AssetsTimeInvariant):

    # Tasks

    @task
    def combined_global_and_conus_meshes(self):
        path = self.rundir / "latentx2.spongex1.combined.sorted.npz"
        yield self.taskname("combined global and CONUS meshes {path}")
        yield Asset(path, path.is_file)
        yield None
        gmesh = _global_latent_grid()
        cmesh = _conus_latent_grid(xds=cds)
        coords = _combined_global_and_conus_meshes(gmesh, cmesh)
        np.savez(
            path,
            lon=coords["lon"],
            lat=coords["lat"]
        )

    @task
    def conus_data_grid(self):
        path = self.rundir / "hrrr_15km.nc"
        yield self.taskname(f"CONUS data grid {path}")
        yield Asset(path, path.is_file)
        yield None
        hrrr = sources.AWSHRRRArchive(
            t0={"start": "2015-01-15T00", "end": "2015-01-15T06", "freq": "6h"},
            fhr={"start": 0, "end": 0, "step": 6},
            variables=["orog"]
        )
        hds = hrrr.open_sample_dataset(
            dims={"t0": hrrr.t0[0], "fhr": hrrr.fhr[0]},
            open_static_vars=True,
            cache_dir=rundir / ".cache"
        )
        hds = hds.rename({"latitude": "lat", "longitude": "lon"})
        # Get bounds as vertices.
        hds = hds.cf.add_bounds(["lat", "lon"])
        for key in ["lat", "lon"]:
            corners = cfxr.bounds_to_vertices(
                bounds=hds[f"{key}_bounds"],
                bounds_dim="bounds",
                order=None,
            )
            hds = hds.assign_coords({f"{key}_b": corners})
            hds = hds.drop_vars(f"{key}_bounds")
        hds = hds.rename({"x_vertices": "x_b", "y_vertices": "y_b"})
        # Get the nodes and bounds by subsampling.
        hds = hds.isel(
            x=slice(None, -4, None),
            y=slice(None, -4, None),
            x_b=slice(None, -4, None),
            y_b=slice(None, -4, None),
        )
        chds = hds.isel(
            x=slice(2, None, 5),
            y=slice(2, None, 5),
            x_b=slice(0, None, 5),
            y_b=slice(0, None, 5),
        )
        chds = chds.drop_vars("orog")
        chds.to_netcdf()

    @task
    def global_data_grid(self):
        path = self.rundir / "global_one_degree.nc"
        yield self.taskname(f"global data grid {path}")
        yield Asset(path, path.is_file)
        yield None
        ds = xesmf.util.grid_global(1, 1, cf=True, lon1=360)
        ds = ds.drop_vars("latitude_longitude")
        ds = ds.sortby("lat", ascending=False) # GFS goes north -> south
        ds.to_netcdf(path)
        
    # @property
    # def output(self) -> dict[str, list[Path]]:
    #     """
    #     Returns a description of the file(s) created when this component runs.
    #     """
    #     cfg = self.config["namelist"]["update_values"]["config"]
    #     halo = cfg.get("halo")
    #     ns = [0, halo] if halo else [0]
    #     keys = [m[1] for key in cfg if (m := re.match(r"^input_(.*)_file$", key))]
    #     return {key: [self.rundir / f"{key}.tile7.halo{n}.nc" for n in ns] for key in keys}

    @collection
    def provisioned_rundir(self):
        yield self.taskname("provisioned run directory")
        yield [
            self.combined_global_and_conus_meshes(),
            self.conus_data_grid(),
            self.global_data_grid()
        ]

    # Public methods

    @classmethod
    def driver_name(cls) -> str:
        return "EAGLE Data"

    # Private methods

    def _combined_global_and_conus_meshes(self, gds, cds):
        glon, glat = np.meshgrid(gmesh["lon"], gmesh["lat"])
        mask = cutout_mask(
            lats=cds["lat"].values.flatten(),
            lons=cds["lon"].values.flatten(),
            global_lats=glat.flatten(),
            global_lons=glon.flatten(),
            min_distance_km=0,
        )
        # Combine.
        lon = np.concatenate([glon.flatten()[mask], cds["lon"].values.flatten()])
        lat = np.concatenate([glat.flatten()[mask], cds["lat"].values.flatten()])
        # Sort, following exactly what anemoi graphs does for the dat.
        coords = np.stack([lon, lat], axis=-1)
        order = get_coordinates_ordering(coords)
        lon = coords[order, 0]
        lat = coords[order, 1]
        return {"lon": lon, "lat": lat}

    def _conus_latent_grid(self, xds, trim=10, coarsen=2):
        mesh = xds[["lat_b", "lon_b"]].isel(
            x_b=slice(trim, -trim - 1, coarsen),
            y_b=slice(trim, -trim - 1, coarsen),
        )
        mesh = mesh.rename(
            {
                "lat_b": "lat",
                "lon_b": "lon",
                "x_b": "x",
                "y_b": "y",
            }
        )
        return mesh

    def _global_latent_grid(self):
        """
        For the high-res version, this will process the original grid. However, since the data grid
        is on an xESMF generated grid, it works out just fine to generate another xESMF grid here.
        """
        mesh = xesmf.util.grid_global(2, 2, cf=True, lon1=360)
        mesh = mesh.drop_vars("latitude_longitude")
        return mesh
