import path_setup 
import geopandas as gpd
import matplotlib.pyplot as plt
import rioxarray
import numpy as np
import xarray as xr
from rasterstats import zonal_stats, point_query
from geocube.api.core import make_geocube
import pandas as pd
import seaborn


from pathlib import Path
from functools import lru_cache
from src.config import *
import calendar

scenes = sorted(p.name for p in Path(PROCESSED_DIR).iterdir() if p.is_dir())
scene_names = []

for scene in scenes:
    year = scene[:4]
    month_nb = int(scene[4:6])
    month_name = calendar.month_name[month_nb]
    scene_names.append(month_name + ' ' + year)

scene_mapping = {k: v for k, v in zip(scenes, scene_names)}

# df_lst_ndvi = pd.read_parquet('../data/processed/20190729_20200827/lst_ndvi.parquet.gzip')
# gdf_nb_temperature = gpd.read_file('../data/processed/20190729_20200827/temperature.geojson')

@lru_cache(maxsize=None)
def load_nta(scene) :
    gdf = gpd.read_file(PROCESSED_DIR / scene / "temperature.geojson")
    gdf["nb_id"] = gdf["nb_id"].astype(int)
    return gdf

@lru_cache(maxsize=None)
def load_pixels(scene):
    return pd.read_parquet(PROCESSED / scene / "lst_ndvi.parquet.gzip")




