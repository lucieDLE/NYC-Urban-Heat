# NYC-Urban-Heat
Analyzing the relationship between urban vegetation and surface temperature across NYC neighborhoods (NTAs), using Landsat 8 data.

Core questions:
- Do greener neighborhoods stay cooler in hot summer?
- which neighborhoods are most and least heat-exposed? 


### 1. Data Sources

- [**Landsat 8/9 satellite imagery**](https://earthexplorer.usgs.gov):
Collection: C2 Level 2
Region: Path 013/Row 032. 
Time Period: June-September
Cloud cover range: [0%, 10%]

Bands: 
    - ST_B10 (LST), 
    - SR_B4/B5 (NDVI), 
    - QA_PIXEL (cloud mask).

Scale factors: temp = raw×0.00341802 + 149.0 − 273.15 (°C); reflectance = raw×0.0000275 − 0.2. 

- [**City neighborhood boundaries**](https://data.cityofnewyork.us/City-Government/2020-Neighborhood-Tabulation-Areas-NTAs-/9nt8-h7nd/about_data)

- **City Demographic per NTA**


### 2. Data Processing
scalin all data to get temperatures/reflectance:
- temp = raw×0.00341802 + 149.0 − 273.15 (°C)
- reflectance = raw×0.0000275 − 0.2. 

LST stands for Land Surface Temperature, BT for Brightness Temperature:
NDVI stands for Normalized Difference Vegetation Index:
- ndvi = (NIR - RED) / (NIR+RED)


Neighborhood IDs rasterized via make_geocube(..., like=lst_celsius) so all layers share one grid; merged with xr.merge (aligns by coordinate, no coordinate join), flattened to one row per pixel.
Aggregated to per-NTA GeoDataFrame gdf_nb_temperature with lst/ndvi mean/std/min/max. nb_id = borocode×100 + within-borough counter.



References
Brightness Temperature (BT) is not the Land Surface Temperature (LST), we need to compute it using equation:
* [1] https://www.researchgate.net/post/LST_from_ST_B10_data 
* [2] https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature
* https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/LSDS-1328_Landsat8-9_OLI-TIRS-C2-L2_DFCB-v7.pdf
* https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/LSDS-2082_L9-Data-Users-Handbook_v1.pdf
- https://www.earthdata.nasa.gov/topics/land-surface/normalized-difference-vegetation-index-ndvi




### Key findings

[-] LST vs NDVI correlation is scale-dependent: pixel level r≈ ___ , all-neighborhoods r≈ ____ , residential-only r≈ ___  (#TODO)
[x] Hottest residential NTAs cluster in southeast Queens. Coolest: Todt Hill, Riverdale.
[x] lst_std only meaningful conditioned on the mean: hot + low-std (evenly hot, no refuge) is the worst case
[x] Within-neighborhood pixel correlation map was tried and dropped — it's blind to parks (no internal NDVI variance → r≈0) and only measures gradients in mixed neighborhoods. Not dashboard-worthy.
