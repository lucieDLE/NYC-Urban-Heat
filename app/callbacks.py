import path_setup  # noqa: F401

import json
from dash import Input, Output, callback, Patch, callback_context

from data import load_nta, load_pixels, compute_indicators
import figures 

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
    
    return f"{ind['Pearson']:.2f}"

@callback(
    Output(component_id="scatter-fig", component_property="figure"),
    Input("scene-dropdown", "value")
    )
def update_scatter_graph(value):

    gdf = load_nta(value)
    df  = load_pixels(value)

    df = df.dropna()

    ind = compute_indicators(gdf, load_pixels(value))
    slope, intercept = ind['Polyfit']

    fig = figures.make_scatter_lst_ndvi(df, slope, intercept, ind['Pearson'])

    return fig


@callback(
    Output(component_id="scatter-rcoff", component_property="children"),
    Output(component_id="scatter-slope", component_property="children"),
    Input("scene-dropdown", "value")
    )
def update_scatter_stats(value):

    gdf = load_nta(value)

    ind = compute_indicators(gdf, load_pixels(value))
    slope, intercept = ind['Polyfit']

    return f"{ind['Pearson']:.2f}", f"{slope / 10:.2f} °C"

@callback(
    Output(component_id="map-lst", component_property="figure"),
    Output(component_id="map-ndvi", component_property="figure"),
    Input("scene-dropdown", "value"))
def update_choropleth(value):
    gdf = load_nta(value)

    lst_fig  = figures.make_cloropleth_map(gdf, 'lst_mean')
    ndvi_fig = figures.make_cloropleth_map(gdf, 'ndvi_mean')

    return lst_fig, ndvi_fig