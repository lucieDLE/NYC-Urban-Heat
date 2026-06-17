# NYC-Urban-Heat


### 1. Data Sources

- [**Landsat 8/9 satellite imagery**](https://earthexplorer.usgs.gov)

- [**City neighborhood boundaries**](https://data.cityofnewyork.us/City-Government/2020-Neighborhood-Tabulation-Areas-NTAs-/9nt8-h7nd/about_data)


- [**Green spaces (parks, forests)**](https://data.cityofnewyork.us/Recreation/Parks-Properties/enfh-gkve/data_preview)


### 2. Data Processing
NDVI stands for Normalized Difference Vegetation Index:
- ndvi = (NIR - RED) / (NIR+RED)
- https://www.earthdata.nasa.gov/topics/land-surface/normalized-difference-vegetation-index-ndvi


https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/LSDS-1328_Landsat8-9_OLI-TIRS-C2-L2_DFCB-v7.pdf
https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/LSDS-2082_L9-Data-Users-Handbook_v1.pdf


clipped_data[0].max().item() --> 52,538

Brightness Temperature (BT) is not the Land Surface Temperature (LST), we need to compute it using equation:
* [1] https://www.researchgate.net/post/LST_from_ST_B10_data 
* [2] https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature
