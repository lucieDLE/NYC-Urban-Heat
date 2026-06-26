---
title: NYC Urban Heat
emoji: 🌿
colorFrom: green
colorTo: green
sdk: docker
app_port: 7860
pinned: false
short_description: relationships between green space and heat in NYC
---

# NYC-Urban-Heat
Analyzing the relationship between urban vegetation and surface temperature across NYC neighborhoods (NTAs), using Landsat 8 data.

Core questions:
- Do greener neighborhoods stay cooler in hot summer?
- which neighborhoods are most and least heat-exposed? 


## Key findings

- LST and NDVI are negatively correlated at every scale: more vegetation means lower surface temperature.
- Hottest residential neighborhoods cluster in Queens/Bronx; coolest are Todt Hill (Staten Island).
- High mean temperature + low std deviation ("evenly hot, no refuge") is the worst heat exposure pattern.


## Setup

```bash
python -m venv geoproj
source geoproj/bin/activate
pip install -r requirements.txt
```



## Data

### 1. Satellite imagery (Landsat 8)

Download from [USGS EarthExplorer](https://earthexplorer.usgs.gov):

- Collection: C2 Level 2
- Path/Row: 013/032 (covers New York City)
- Period: June–September (summer scenes only)
- Cloud cover: 0–10%
- Bands needed: `ST_B10` (LST), `SR_B4` (red), `SR_B5` (NIR), `SR_B3` (green), `QA_PIXEL`


### 2. Neighborhood boundaries (NTAs)

Download the 2020 NTA GeoJSON from the [NYC Open Data portal](https://data.cityofnewyork.us/City-Government/2020-Neighborhood-Tabulation-Areas-NTAs-/9nt8-h7nd/about_data) 

### 3. Demographics

A pre-processed demographic CSV (race/ethnicity by NTA from the 2020 Census) is already included at `data/processed/nyc_nta_race_ethnicity_2020_exclusive.csv`. It was created from the [NYC Department of Ciy Planning](https://www.nyc.gov/content/planning/pages/resources/datasets/decennial-census)


## Preprocessing

After placing raw satellite files in `data/raw/`, run the preprocessing pipeline to generate per-scene GeoJSON and Parquet files:

```bash
python src/preprocess.py
```

This script:
1. Applies cloud masking using the `QA_PIXEL` band.
2. Converts raw DN values to Land Surface Temperature (°C) and NDVI/NDWI.
3. Aggregates pixel-level values to neighborhood (NTA) statistics.
4. Writes outputs to `data/processed/<scene_id>/`:
   - `temperature.geojson`: per-NTA LST and NDVI statistics
   - `lst_ndvi.parquet.gzip`: pixel-level sample for scatter plots

Scenes are identified by their date range (e.g. `20230809_20230812`). Add or remove scene IDs in the `scenes` list at the top of `src/preprocess.py`.


## Running the app

```bash
python app/app.py
```

Open [http://localhost:8050](http://localhost:8050) in your browser.

The dropdown at the top of the dashboard lets you switch between processed satellite scenes.


## Data sources

- [USGS EarthExplorer - Landsat Collection 2 Level 2](https://earthexplorer.usgs.gov)
- [NYC Open Data - 2020 Neighborhood Tabulation Areas](https://data.cityofnewyork.us/City-Government/2020-Neighborhood-Tabulation-Areas-NTAs-/9nt8-h7nd/about_data)
- [Landsat Collection 2 Surface Temperature product guide](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature)
- [NASA EARTHDATA - NDVI](https://www.earthdata.nasa.gov/topics/land-surface/normalized-difference-vegetation-index-ndvi)
- [NYC Department of Ciy Planning - Decennial Census Data](https://www.nyc.gov/content/planning/pages/resources/datasets/decennial-census)
