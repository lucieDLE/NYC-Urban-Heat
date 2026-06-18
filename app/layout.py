import path_setup  # noqa: F401
import re

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def build_layout():

    dark_mode_switch =  html.Span([
            dbc.Label(className="fa fa-sun", html_for="switch"),
            dbc.Switch(id="switch-theme", value=True, className="d-inline-block ms-1", persistence=True),
            dbc.Label(className="fa fa-moon", html_for="switch"),
        ])

    ribbon = html.Div([
            html.H1("Exploring NYC Urban Heat"), 
            dark_mode_switch,
        ], className="ribbon")

    subtitle = html.Div([
        html.H5("Do neighborhoods with more green space stay cooler in summer?"),
        ], className='subtitle'
    )

    rail = html.Aside(html.Nav([
        html.A('overview', href="#overview",id="overview",),
        html.A('Vegetation & heat', href="#veg",id="veg",),
        html.A('The maps', href="#maps",id="maps",),
        html.A('where', href="#ranks",id="ranks",),
        html.A('Heat risk', href="#risk",id="risk",),
        html.A('Methodology', href="#method",id="method",),
    ], className='nav'), className="rail")

    main = html.Main([
        html.Section(
            id='overview', 
            children = [
                html.H5("Overview"),
                html.H1("Does greener mean cooler?"),
                html.P("text")
            ], className='section'),
        html.Section(
            id='maps', 
            children = [
                html.H5("The maps"),
                html.H1("Visualize the data"),
                html.P("text")
        ],className='section'),
        html.Section(
            id='veg', 
            children = [
                html.H5("Relationship"),
                html.H1("Vegetation & heat"),
                html.P("text")
        ],className='section'),
        html.Section(
            id='ranks', 
                    children = [
                html.H5("Where"),
                html.H1("Heat and people"),
                html.P("text")
                ],
            className='section'
        ),
        html.Section(
            id='risk', 
                    children = [
                html.H5("risk"),
                html.H1("Heat inequality"),
                html.P("text")
                ],
            className='section'
        ),
        html.Section(
            id='method', 
                    children = [
                html.H5("Method"),
                html.H1("Method and References"),
                html.P("text")
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