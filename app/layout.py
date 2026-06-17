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

    layout = dbc.Container( fluid=True,
                                id="page-wrapper",
                                children=[
                                    dcc.Store(id="viewport-width", data=1200),
                                    html.Div([
                                        html.H4("Exploring NYC urban heat"),
                                        dark_mode_switch,
                                    ],className='app-header'
                                    ),
                                    dcc.Tabs([
                                        dcc.Tab(label='Beyond the AQI',),
                                        dcc.Tab(label='Beyond the AQI',),
                                        dcc.Tab(label='Beyond the AQI',),
                                        ]),
                                    ],
                                )

    return layout