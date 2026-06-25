import path_setup  # noqa: F401
import re

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src import config
from data import dict_scene_mapping, list_scene_dropdown
import display_text

def text_card(title, sub):
    return html.Div([
            html.Div(title),
            html.P(sub),
        ], className="text-card",
    )


def stat_card(title, value, sub, stat_id, stat_location, accent="hsl(120, 50%, 37%)", card_id='card'):
    return html.Div([
            html.Div(title),
            html.H5(value, id=stat_id), 
            html.P(sub, id=stat_location),
        ], className=card_id, style={"--bar": accent}
    )

def graph_card(fig_id, figure=None, classname="chart-card", modebar = True):
    return html.Div(
        dcc.Graph(id=fig_id, figure=figure, responsive=True, config={"displayModeBar": modebar}),
        className=classname
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

    finding = html.Div([
        html.Div(className="scale"),          # the gradient bar
        html.P([
            html.B("Yes."),
            " At the land surface, temperature falls about ",
            html.B(id="finding-value", children="—"), 
            " for every 0.1 gain in NDVI, and the bare, paved blocks are the ones that heat up.",
        ]),
    ], className="finding")

    ribbon = html.Div([
            html.H1("Exploring NYC Urban Heat"), 
            dark_mode_switch,
        ], className="ribbon")

    subtitle = html.Div([
        html.H5("Do neighborhoods with more green space stay cooler in summer?"),
        ], className='subtitle'
    )

    rail = html.Aside(html.Nav([
        html.A([html.I(className="fa-solid fa-calendar-day"), 'overview'], href="#overview"),
        html.A([html.I(className="fa-solid fa-satellite"), 'The maps'], href="#maps"),
        html.A([html.I(className="fa-solid fa-leaf"), 'Vegetation & heat'], href="#veg"),
        html.A([html.I(className="fa-solid fa-location-dot"), 'where'], href="#ranks"),
        html.A([html.I(className="fa-solid fa-building-user"), 'Heat inequality'], href="#risk"),
        html.A([html.I(className="fa-solid fa-people-group"), 'Demographics'], href="#demographics"),
        html.A([html.I(className="fa-solid fa-book-bookmark"), 'Methodology'], href="#method"),
    ], className='nav'), className="rail")

    main = html.Main([
        html.Section(
            id='overview', 
            children = [
                html.Div("Overview", className="eyebrow"),
                html.H1("Does greener mean cooler?"),
                html.P(display_text.OVERVIEW_DESCRIPTION,className="section-description"),
                dropdown,
                finding,
                html.Div([
                    stat_card("City mean surface temp", "—", "all areas", "kpi-mean", "loc-mean", accent="#E9C158"),
                    stat_card("Coolest Temperature", "—", "neighborhood", "kpi-min", "location-min", accent="#3D86C0"),
                    stat_card("Hottest Temperature", "—", "neighborhood", "kpi-max", "location-max", accent="#CF4226"),
                    stat_card("Vegetation-heat coeff", "—", "Pearson correlation", "kpi-corr", "loc-corr", accent="hsl(120, 50%, 37%)"),
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
                html.H1("Vegetation & heat Correlation"),
                html.P("text",className="section-description"),
                html.Div([
                    graph_card("scatter-fig", modebar = False),
                    html.Div([
                        stat_card("Pixel Level", "—", "Pearson r", "scatter-rcoff", "scatter-rcoff-loc"),
                        stat_card("Residential only", "to come", "detail", "scatter-residential", "corr-residential-loc"),
                        stat_card("All Neighborhoods", "—", "°C per 0.1 NDVI", "scatter-parks", "corr-slope-loc"),
                    ], className="panel-side"),
                ], className="panel")

        ],className='section'),
        html.Section(
            id='ranks', 
            children = [
                html.Div("Where", className="eyebrow"),
                html.H1("Heat and people"),
                html.P("text", className="section-description"),
                html.Div([
                    dcc.RadioItems(
                        id="ranking-scope",
                        options=[
                            {"label": "Residential only", "value": "res"},
                            {"label": "All neighborhoods", "value": "all"},
                        ],
                        value="all",          # default selection (also fires the callback on load)
                        inline=True,          # lay the two options side by side
                        className="scope-toggle",
                    ),
                    graph_card("ranking-fig", modebar = False),
                    ], className="rank-chart",)
                ],
            className='section'
        ),
        html.Section(
            id='risk', 
            children = [
                html.Div("risk", className="eyebrow"),
                html.H1("Heat inequality"),
                html.P("text",className="section-description"),
                graph_card("risk-scatter-fig", modebar = False),
                ],
            className='section'
        ),

        html.Section(
            id='demographics', 
            children = [
                html.Div("Demographics", className="eyebrow"),
                html.H1("Explore the communities at risk"),
                html.Div([
                    dcc.RadioItems(
                        id="demo-layer",
                        options=[
                            {"label": "Asian",             "value": "asian_pct"},
                            {"label": "Black",             "value": "black_pct"},
                            {"label": "Hispanic",          "value": "hispanic_pct"},
                            {"label": "White",             "value": "white_pct"},
                            {"label": "Predominant group", "value": "predominant_group"},
                            ],
                        value="hispanic_pct",
                        inline=True,
                        className="scope-toggle",
                    ),
                    graph_card("demographics-map", classname='demographic-chart')
                ], className='rank-chart')
                ],
            className='section'
        ),
        html.Section(
            id='method', 
                    children = [
                html.Div("Method", className="eyebrow"),
                html.H1("Method and References"),
                html.Div([
                    text_card("Land Surface Temperature", "detail"),
                    text_card("NDVI", "detail"),

                    text_card("Aggregation", "detail"),
                    text_card("Aggregation", "detail"),

                    text_card("Data", "detail"),
                    text_card("References", "detail"),
                    ],className='method-cards')
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