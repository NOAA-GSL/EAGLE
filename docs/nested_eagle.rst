=================
Nested Eagle
=================

The nested-eagle model is a prototype model trained on global NOAA Global Forecast System (GFS) data 
with High Resolution Rapid Refresh (HRRR) data over the Contiguous United States (CONUS). 
This builds on previous work from Met Norway (Nipen et al., 2024, arXiv:2409.02891) by creating a 
nested model with lower resolution global data and high resolution over an area of interest.

TODO - Insert image of nested domain here.

Nested-eagle configurations were created by Tim Smith at NOAA Physical Sciences Laboratory.

Training Data
------------------

Datasets:

- GFS convservatively regridded to 1-degree
- HRRR conservatively regridded to 15-km 

Time period:

- Training dataset: 2015-02-01T06 to 2023-01-31T18
- Validation dataset: 2023-02-01T06 to 2024-01-31T18

Variables:

- Prognostic: gh, u, v, w, t, q, sp, u10, v10, t2m, t_surface, sh2
- Diagnostic: u80, v80, accum_tp (use fhr 6)
- Forcing: lsm, orog, cos_latitude, sin_latitude, cos_longitude, sin_longitude, cos_julian_day, sin_julian_day, cos_local_time, sin_local_time, insolation
- Levels: 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000

Model Architecture
------------------

Encoder: Graph Transformer

Processor: Shifted Window Transformer with 512 channels

Decoder: Graph Transformer

Graph: Used for the encoder and decoder to connect targets to nodes via nearest neighbors (encoder_knn=12, decode_knn=3).
Latent mesh is 4 times more coarse than native data.
