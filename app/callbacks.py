import path_setup  # noqa: F401

import json
from dash import Input, Output, callback, Patch, callback_context

import data 
import figures 

@callback(
    Output(component_id="kpi-mean", component_property="children"),
    Output(component_id="kpi-min", component_property="children"),
    Output(component_id="location-min", component_property="children"),
    Output(component_id="kpi-max", component_property="children"),
    Output(component_id="location-max", component_property="children"),
    Output(component_id="kpi-corr", component_property="children"),
    Output(component_id='finding-value', component_property='children'),

    Output(component_id="map-lst", component_property="figure"),
    Output(component_id="map-ndvi", component_property="figure"),


    Output(component_id="scatter-fig", component_property="figure"),
    Output(component_id="scatter-rcoff", component_property="children"),
    Output(component_id="scatter-residential", component_property="children"),
    Output(component_id="scatter-parks", component_property="children"),

    Output("risk-scatter-fig", "figure"),

    Input("scene-dropdown", "value")
    )
def update_cards(value):
    
    # load data
    gdf = data.load_nta(value)
    df  = data.load_pixels(value)
    ind = data.get_indicators(value)
    
    gdf['lst_mean_dev'] = gdf['lst_mean'] - gdf['lst_mean'].mean()

    gdf_residential = data.filter_on_area(gdf, '0')
    gdf_residential['lst_mean_dev'] = gdf_residential['lst_mean'] - gdf_residential['lst_mean'].mean()

    
    px, res, park = ind['Pearson'].values()
    px_rcoff, res_rcoff, parks_rcoff = f"{px:.2f}", f"{res:.2f}", f"{park:.2f}"

    # section overview - cards
    mean =  f"{ind['City-Level Temperature']['mean']:.1f} °C"

    min_vals = ind['City-Level Temperature']['min']
    min_val, min_loc = f"{min_vals[1]:.1f} °C", min_vals[0]

    max_vals = ind['City-Level Temperature']['max']
    max_val, max_loc = f"{max_vals[1]:.1f} °C", max_vals[0]
    
    p_corr = px_rcoff
    slope, intercept = ind['Polyfit']['all']
    slope_txt = f"{abs(slope) / 10:.1f} °C"
    # section overview return : mean, min_val, min_loc, max_val, max_loc, px_rcoff, slope_txt

    # section display map 
    lst_fig  = figures.make_cloropleth_map(gdf_residential, 'lst_mean_dev')
    ndvi_fig = figures.make_cloropleth_map(gdf, 'ndvi_mean')
    # section display maps return: lst_fig, ndvi_fig

    # section ndvi - lst relationship
    scatter_lst_ndvi = figures.make_scatter_lst_ndvi(df, slope, intercept, ind['Pearson']['all'])
    # section ndvi - lst return : px_rcoff, res_rcoff, parks_rcoff

    # section scatter inequality
    inequality_fig = figures.make_inequality_scatter(gdf_residential, gdf)

    return (
        mean, min_val, min_loc, max_val, max_loc, px_rcoff, slope_txt, 
        lst_fig, ndvi_fig, 
        scatter_lst_ndvi, px_rcoff, res_rcoff, parks_rcoff, 
        inequality_fig
    )

@callback(
    Output(component_id="ranking-fig", component_property="figure"),
    Input("scene-dropdown", "value"),
    Input("ranking-scope", "value"),
    )
def update_scatter_stats(scene, scope):

    ind = data.get_indicators(scene)
    if scope == 'res':
        fig = figures.make_ranking_bar(ind['ranking Hottest/Coolest Residential'])
    else:
        fig = figures.make_ranking_bar(ind['ranking Hottest/Coolest'])

    return fig



@callback(
    Output("demographics-map", "figure"),
    Input("scene-dropdown", "value"),
    Input("demo-layer", "value"),
)
def update_demographics_map(scene, layer):
    gdf = data.load_demographics(scene)
    if layer == "predominant_group":
        return figures.make_predominant_map(gdf)
    return figures.make_demographics_map(gdf, layer)