import path_setup  # noqa: F401
import re

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src import config
from data import dict_scene_mapping, list_scene_dropdown
import display_text

def stat_card(title, value, sub, stat_id, stat_location, card_id='card'):
    return html.Div([
            html.Div(title),
            html.H5(value, id=stat_id), 
            html.P(sub, id=stat_location),
        ], className=card_id,
    )

def graph_card(fig_id, figure=None):
    return html.Div(
        dcc.Graph(id=fig_id, figure=figure, responsive=True),
        className="chart-card"
    )

def build_layout():

    dark_mode_switch =  html.Span([
            dbc.Label(className="fa fa-sun", html_for="switch"),
            dbc.Switch(id="switch-theme", value=True, className="d-inline-block ms-1", persistence=True),
            dbc.Label(className="fa fa-moon", html_for="switch"),
        ])

    dropdown = dcc.Dropdown(
        options=list_scene_dropdown,
        value=config.DEFAULT_SCENE,
        id="scene-dropdown",
        )

    ribbon = html.Div([
            html.H1("Exploring NYC Urban Heat"), 
            dark_mode_switch,
        ], className="ribbon")

    subtitle = html.Div([
        html.H5("Do neighborhoods with more green space stay cooler in summer?"),
        ], className='subtitle'
    )

    rail = html.Aside(html.Nav([
        html.A('overview', href="#overview"),
        html.A('Vegetation & heat', href="#veg"),
        html.A('The maps', href="#maps"),
        html.A('where', href="#ranks"),
        html.A('Heat risk', href="#risk"),
        html.A('Methodology', href="#method"),
    ], className='nav'), className="rail")

    main = html.Main([
        html.Section(
            id='overview', 
            children = [
                html.Div("Overview", className="eyebrow"),
                html.H1("Does greener mean cooler?"),
                html.P(display_text.OVERVIEW_DESCRIPTION,className="section-description"),
                html.Div("answer using correlation/polyfit", className="text-card"),
                dropdown,
                html.Div([
                    stat_card("City mean surface temp",      "—", "all areas",    "kpi-mean", "loc-mean"),
                    stat_card("Coolest Temperature",         "—", "neighborhood", "kpi-min",  "location-min"),
                    stat_card("Hottest Temperature",         "—", "neighborhood", "kpi-max",  "location-max"),
                    stat_card("Vegetation-heat correlation", "—", "Pearson r",    "kpi-corr", "loc-corr"),
                    ],className='overview-card-section')
            ], className='section'),
        html.Section(
            id='maps', 
            children = [
                html.Div("The maps", className="eyebrow"),
                html.H1("Visualize the data"),
                html.P("text",className="section-description"),
                html.Div([
                    graph_card("map-lst"),
                    graph_card("map-ndvi"),
                ], className="maps-grid"),
        ],className='section'),
        html.Section(
            id='veg', 
            children = [
                html.Div("Relationship", className="eyebrow"),
                html.H1("Vegetation & heat"),
                html.P("text",className="section-description"),
                html.Div([
                    graph_card("scatter-fig"),
                    html.Div([
                        stat_card("Vegetation–heat correlation", "—", "Pearson r", "scatter-rcoff", "scatter-rcoff-loc"),
                        stat_card("Residential impact", "to come", "detail", "scatter-residential", "corr-residential-loc"),
                        stat_card("Cooling effect", "—", "°C per 0.1 NDVI", "scatter-slope", "corr-slope-loc"),
                    ], className="panel-side"),
                ], className="panel")

        ],className='section'),
        html.Section(
            id='ranks', 
                    children = [
                html.Div("Where", className="eyebrow"),
                html.H1("Heat and people"),
                html.P("text", className="section-description"),

                ],
            className='section'
        ),
        html.Section(
            id='risk', 
                    children = [
                html.Div("risk", className="eyebrow"),
                html.H1("Heat inequality"),
                html.P("text",className="section-description")
                ],
            className='section'
        ),
        html.Section(
            id='method', 
                    children = [
                html.Div("Method", className="eyebrow"),
                html.H1("Method and References"),
                html.P("text",className="section-description")
                ],
            className='section'
        ),

    ], id="scroller")

    shell = html.Div([rail, main], className="shell")   # the row

    layout = dbc.Container( fluid=True,
                                id="page-wrapper",
                                children=[
                                    dcc.Store(id="viewport-width", data=1200),
                                    ribbon, 
                                    subtitle,
                                    shell,
                                    ],
                                )

    return layout