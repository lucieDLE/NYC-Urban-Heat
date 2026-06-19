import path_setup  # noqa: F401

import json
from dash import Input, Output, callback, Patch, callback_context

from data import load_nta, load_pixels, compute_indicators

@callback(
    Output(component_id="kpi-mean", component_property="children"),
    Input("scene-dropdown", "value")
    )
def update_mean_card(value):
    gdf = load_nta(value)
    ind = compute_indicators(gdf, load_pixels(value))
    
    return f"{ind['City-Level Temperature']['mean']:.1f} °C"

@callback(
    Output(component_id="kpi-min", component_property="children"),
    Output(component_id="location-min", component_property="children"),
    Input("scene-dropdown", "value")
    )

def update_min_card(value):
    gdf = load_nta(value)
    ind = compute_indicators(gdf, load_pixels(value))

    min_vals = ind['City-Level Temperature']['min']
    return f"{min_vals[1]:.1f} °C", min_vals[0]



@callback(
    Output(component_id="kpi-max", component_property="children"),
    Output(component_id="location-max", component_property="children"),
    Input("scene-dropdown", "value")
    )
def update_max_card(value):
    gdf = load_nta(value)
    ind = compute_indicators(gdf, load_pixels(value))
    
    max_vals = ind['City-Level Temperature']['max']
    return f"{max_vals[1]:.1f} °C", max_vals[0]



@callback(
    Output(component_id="kpi-corr", component_property="children"),
    Input("scene-dropdown", "value")
    )
def update_ndvi_corr_card(value):
    gdf = load_nta(value)
    ind = compute_indicators(gdf, load_pixels(value))
    
    return f"{ind['Pearson']:.1f}"
