import numpy as np
import geopandas as gpd
import rioxarray
import xarray as xr
from geocube.api.core import make_geocube
import pandas as pd 
from pathlib import Path

neighborhoods = 'data/raw/2020_Neighborhood_Tabulation_Areas_(NTAs)_20260610.geojson'
gdf_neigbhorhood = gpd.read_file(neighborhoods)

# create neigborhood gdf (copy so we can safely add columns)
sub_gdf_nb = gdf_neigbhorhood[['borocode', 'boroname', 'ntaname', 'ntatype', 'shape_leng', 'shape_area', 'nta2020', 'geometry' ]].copy()
sub_gdf_nb['borocode'] = sub_gdf_nb['borocode'].astype(int)
sub_gdf_nb["nb_id"] = sub_gdf_nb["borocode"]*100 + sub_gdf_nb.groupby("borocode").cumcount() + 1


scenes = [
    '20190729_20200827',
    '20220806_20220817',
    '20230809_20230812',
    '20250830_20250903',
]

# preprocess all scenes
for scene in scenes:

    Path("data/processed/" + scene).mkdir(parents=True, exist_ok=True)

    scene_name = f'LC08_L2SP_013032_{scene}_02_T1'

    temperature_file = 'data/raw/' + scene_name + '/' + scene_name + '_ST_B10.TIF'
    qa_file =  'data/raw/' + scene_name + '/' + scene_name + '_QA_PIXEL.TIF'

    red_file = 'data/raw/' + scene_name + '/' + scene_name + '_SR_B4.TIF'
    nir_file = 'data/raw/' + scene_name + '/' + scene_name + '_SR_B5.TIF'
    green_file = 'data/raw/' + scene_name + '/' + scene_name + '_SR_B3.TIF'

    ds_temperature = rioxarray.open_rasterio(temperature_file, masked=True)

    qa = rioxarray.open_rasterio(qa_file, masked=False)
    red_band = rioxarray.open_rasterio(red_file, masked=True) * 0.0000275 - 0.2
    nir_band = rioxarray.open_rasterio(nir_file, masked=True) * 0.0000275 - 0.2
    green_band =rioxarray.open_rasterio(green_file, masked=True) * 0.0000275 - 0.2

    # Bit 3 = cloud, Bit 4 = cloud shadow --> remove all clouds from temperature
    qa_int16 = qa.data.astype('int16')
    cloud_mask = (qa_int16 & 0b00001000) | (qa_int16 & 0b00010000)
    ds_temperature_masked = ds_temperature.where(cloud_mask == 0)


    # compute temperature (C) layer
    ds_temperature_proj = ds_temperature_masked.rio.reproject("EPSG:4326") # same as gdfs

    # Clip the raster to the shape -> .geometry act as a mask
    lst_raw = ds_temperature_proj.rio.clip(gdf_neigbhorhood.geometry, gdf_neigbhorhood.crs)

    # Apply scale factor → convert to Celsius
    lst_celsius = lst_raw * 0.00341802 + 149.0 - 273.15
    lst_celsius.name = "temperature_celsius"


    ## compute NDVI layer
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    ndvi.name = "ndvi"

    ndvi = ndvi.rio.reproject("EPSG:4326")
    ndvi = ndvi.rio.clip(gdf_neigbhorhood.geometry, gdf_neigbhorhood.crs)

    # compute NDWI layer
    ndwi = (green_band - nir_band) / (green_band + nir_band)
    ndwi.name = "ndwi"

    ndwi = ndwi.rio.reproject("EPSG:4326")
    ndwi = ndwi.rio.clip(gdf_neigbhorhood.geometry, gdf_neigbhorhood.crs)

    max_wv = np.maximum(ndvi, ndwi) 
    max_wv.name = 'ndvi'

    ndvi_matched = max_wv.rio.reproject_match(lst_celsius)
    ds_lst_ndvi = xr.merge([
        lst_celsius.rename("lst"),
        ndvi_matched.rename("ndvi"),
    ])

    df_lst_ndvi = ds_lst_ndvi.to_dataframe().reset_index().dropna(subset=["lst", "ndvi"])
    df_lst_ndvi = df_lst_ndvi[(df_lst_ndvi["ndvi"] >0) & (df_lst_ndvi["ndvi"] <= 1)]
    # sample for the scatter slice; guard against fewer rows than the target
    df_lst_ndvi = df_lst_ndvi.sample(n=min(300000, len(df_lst_ndvi)), random_state=0)

    output_fp = 'data/processed/' + scene +  "/lst_ndvi.parquet.gzip"
    df_lst_ndvi.to_parquet(output_fp, compression="gzip")
    # pd.read_parquet("df.parquet.gzip")


    neighborhood_ds = make_geocube(
        vector_data=sub_gdf_nb,
        measurements=["borocode", 'nb_id'],
        like=lst_celsius,
    )

    ds_all = xr.merge([ 
        lst_celsius.rename("lst"),
        ndvi_matched.rename("ndvi"),
        neighborhood_ds["nb_id"]
        ])
    
    df_all = ds_all.to_dataframe().reset_index().dropna(subset=["lst", "ndvi", "nb_id"])

    list_correlation = []
    list_index = []
    for nb_id in df_all['nb_id'].unique():

        df_nb = df_all.loc[df_all['nb_id'] == nb_id]
        pearson_coeff = df_nb['lst'].corr(df_nb['ndvi'])

        list_correlation.append(pearson_coeff)
        list_index.append(nb_id)

    df_correlation = pd.DataFrame(data={'nb_id':list_index, 'correlation':list_correlation})


    df_boro_temperature = df_all.groupby('nb_id').agg(
        x = ("x", 'mean'),
        y = ("y", 'mean'),

        lst_mean = ("lst", 'mean'),
        lst_std = ("lst", 'std'),
        lst_min = ("lst", 'min'),
        lst_max = ("lst", 'max'),

        ndvi_mean = ("ndvi", 'mean'),
        ndvi_std = ("ndvi", 'std'),
        ndvi_min = ("ndvi", 'min'),
        ndvi_max = ("ndvi", 'max'),

        ).reset_index()
    
    df_boro_temperature = df_boro_temperature.merge(df_correlation, on='nb_id')

    df_boro_temperature['nb_id'] = df_boro_temperature['nb_id'].astype(int)
    gdf_nb_temperature = sub_gdf_nb.merge(df_boro_temperature, on='nb_id', how="left")

    output_fp = 'data/processed/' + scene +  "/temperature.geojson"
    gdf_nb_temperature.to_file(output_fp)
