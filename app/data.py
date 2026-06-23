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
from display_text import NTA_MAPPING_GRAPH


scenes = sorted(p.name for p in Path(PROCESSED_DIR).iterdir() if p.is_dir())
scene_names = []
dict_scene_mapping = {}
list_scene_dropdown = []
for scene in scenes:
    year = scene[:4]
    month_nb = int(scene[4:6])
    month_name = calendar.month_name[month_nb]
    scene_names.append(month_name + ' ' + year)

for k, v in zip(scenes, scene_names):
    dict_scene_mapping[k]= v
    list_scene_dropdown.append( {'label': v, 'value': k})

def shorten_names(name):
    if len(name) > 30:
        new_name = NTA_MAPPING_GRAPH[name]
        return new_name
    else: return name
    

@lru_cache(maxsize=None)
def load_nta(scene) :
    gdf = gpd.read_file(PROCESSED_DIR / scene / "temperature.geojson")
    gdf["nb_id"] = gdf["nb_id"].astype(int)
    gdf['ntatype_name'] = gdf['ntatype'].apply(lambda x: ntatype_mapping[x])
    gdf['ntaname'] = gdf.apply(lambda row: shorten_names(row['ntaname']), axis=1)

    return gdf

@lru_cache(maxsize=None)
def load_pixels(scene):
    return pd.read_parquet(PROCESSED_DIR / scene / "lst_ndvi.parquet.gzip")


@lru_cache(maxsize=None)
def load_demographics(scene):
    gdf = load_nta(scene)
    df  = pd.read_csv(DEMOGRAPHICS_CSV).rename(columns={"nta_name": "ntaname"})
    df  = df.drop(columns=["geoid", "borough", "nta_type"])
    merged = gdf.merge(df, on="ntaname", how="left")
    return filter_on_area(merged, "0")   # residential only, like the notebook

def filter_on_area(gdf, type_nb):
    return gdf.loc[ gdf.ntatype == type_nb]

def compute_indicators(gdf_temperature, df_lst_ndvi):

    dict_indicators = {}

    pearson_coeff = df_lst_ndvi['lst'].corr(df_lst_ndvi['ndvi'])
    slope, intercept = np.polyfit(df_lst_ndvi["ndvi"], df_lst_ndvi["lst"], 1)


    gdf_residential_temperature = filter_on_area(gdf_temperature, '0')

    df_lst_mean_all = gdf_temperature.sort_values(by=['lst_mean'])[['ntatype_name','boroname', 'ntatype', 'ntaname', 'lst_mean', 'lst_std','ndvi_mean',  'ndvi_std'] ].dropna()
    df_lst_min_max_all = pd.concat([df_lst_mean_all[:3], df_lst_mean_all[-3:]])

    
    df_lst_mean = gdf_residential_temperature.sort_values(by='lst_mean')[ ['ntatype_name','borocode','boroname','ntaname','nb_id', 'lst_mean', 'ndvi_mean']]
    df_lst_min_max_nb = pd.concat([df_lst_mean[:3], df_lst_mean[-3:]])
    

    df_lst_std = gdf_residential_temperature.sort_values(by=['lst_mean', 'ndvi_mean'], ascending=[False, True])[['boroname', 'ntaname', 'lst_mean', 'lst_std','ndvi_mean',  'ndvi_std'] ]
    df_inequality = pd.concat([df_lst_std[:3],df_lst_std[-3:] ])
    
    max_val = gdf_temperature.sort_values(by='lst_mean', ascending=False).iloc[0]
    min_val = gdf_temperature.sort_values(by='lst_mean', ascending=True).iloc[0]

    # City level temperature values for that day
    dict_indicators['City-Level Temperature'] = {
        'mean': gdf_temperature.lst_mean.mean(),
        'min': [min_val['ntaname'], min_val['lst_min'].item()],	
        'max': [max_val['ntaname'], max_val['lst_max'].item()],
    }
    
    # Answer Question 1: Do greener blocks mean cooler?
    dict_indicators['Pearson'] = pearson_coeff
    dict_indicators['Polyfit'] = (slope, intercept)

    # Tile 2: plot Heat beside Green (LST/NDVI mean)
    # plot gdf_type 0 for Heat but all ntatype for NDVI
    dict_indicators['ranking Hottest/Coolest Residential'] = df_lst_min_max_nb


    # Tile 3: Inequality (LST std /NDVI mean)
    dict_indicators['ranking Heat Inequality'] = df_lst_min_max_nb


    # Tile 1: Coolest Neighborhoods
    # ---> parks with low temperature, high ndvi mean 
    dict_indicators['ranking Hottest/Coolest'] = df_lst_min_max_all

    return dict_indicators