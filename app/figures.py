import numpy as np
import plotly.graph_objects as go

COLS_DISPLAY= [
    "ntaname", "boroname",
    "ntatype_name",
    "lst_mean", "lst_std",
    "lst_min", "lst_max",
    "ndvi_mean", "ndvi_std",
    "ndvi_min", "ndvi_max",
    "lst_mean_dev"
    ]

DEMO_GROUP_COLORS = {
      "hispanic":           "#e6550d",  # Oranges mid
      "white":              "#756bb1",  # Purples mid
      "black":              "#3182bd",  # Blues mid
      "asian":              "#31a354",  # Greens mid
  }
DEMO_GROUPS = list(DEMO_GROUP_COLORS.keys())

# What the choropleth can be colored by.
# Each entry: how to label it (dropdown + title), the colorbar text,
# the colorscale, and a fixed range (None = auto-range from the data).
COLOR_OPTIONS = {
    "lst_mean_dev": {
        "label": "Deviation from City-Mean surface temperature",
        "legend": "LST (°C)",
        "colorscale": "RdYlBu_r",
        "zmin": None, "zmax": None,
    },
    "ndvi_mean": {
        "label": "Vegetation (NDVI)",
        "legend": "NDVI",
        "colorscale": "RdYlGn",
        "zmin": -1, "zmax":1, 
    },
    "lst_std": {
        "label": "Temperature variability (heat inequality)",
        "legend": "LST std (°C)",
        "colorscale": "Reds",
        "zmin": None, "zmax": None,
    },
}

DEMO_COLOR_OPTIONS = {
    "hispanic_pct":{
        "label": "Hispanic (%)",
        "legend": "%", 
        "colorscale": "Oranges",
        "zmin": 0, 
        "zmax": 100
        },

    "white_pct":{
        "label": "White (%)", 
        "legend": "%", 
        "colorscale": "Purples", 
        "zmin": 0, 
        "zmax": 100
        },

    "black_pct":{
        "label": "Black (%)", 
        "legend": "%", 
        "colorscale": "Blues", 
        "zmin": 0, 
        "zmax": 100
        },

    "asian_pct":{
        "label": "Asian (%)", 
        "legend": "%", 
        "colorscale": "Greens", 
        "zmin": 0, 
        "zmax": 100
        },

}

def make_cloropleth_map(gdf, column_name, color_options=None):

    opt = (color_options or COLOR_OPTIONS)[column_name]

    gdf_json = gdf.set_index("nb_id").__geo_interface__

    fig = go.Figure(data=go.Choroplethmap(
        geojson=gdf_json,
        locations=gdf["nb_id"],
        featureidkey="id",
        z=gdf[column_name],
        colorscale=opt["colorscale"],
        zmin=opt.get("zmin"), zmax=opt.get("zmax"),   # None → Plotly auto-ranges
        marker_line_color="green",
        marker_line_width=0.5,
        marker_opacity=0.7,
        colorbar=dict(title=dict(text=opt["legend"])),
        customdata=gdf[COLS_DISPLAY],
        hovertemplate=(
            "<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
            "type : %{customdata[2]}<br> <br>"

            "LST Deviation from Mean:  %{customdata[11]:.1f}°C<br>"

            "LST: <br>"
            "       mean:  %{customdata[3]:.1f}°C<br>"
            "       std:   %{customdata[4]:.1f}°C<br>"
            "       min:   %{customdata[5]:.1f}°C<br>"
            "       max:   %{customdata[6]:.1f}°C<br> <br>"

            "NDVI: <br>"
            "       mean: %{customdata[7]:.2f}<br>"
            "       std:  %{customdata[8]:.2f}<br>"
            "       min:  %{customdata[9]:.2f}<br>"
            "       max:  %{customdata[10]:.2f}<extra></extra>"

        ),
    ))

    fig.update_layout(
        margin=dict(t=30, b=0, l=0, r=0),
        title=dict(text=opt["label"], x=0.5, xanchor="center"),
        map=dict(
            # style="carto-voyager",
            center=dict(lat=40.70, lon=-73.95),
            zoom=9,
        ),
    )

    return fig


def make_scatter_lst_ndvi(df_lst_ndvi, slope, intercept, pearson):
    fig = go.Figure()

    nbins=80
    counts, xedges, yedges = np.histogram2d(
        df_lst_ndvi["ndvi"], df_lst_ndvi["lst"], bins=nbins
    )
    counts = counts.T                                   # heatmap wants [y, x]
    z = np.where(counts > 0, np.log10(counts), np.nan)  # log; empty bins → NaN

    xc = 0.5 * (xedges[:-1] + xedges[1:])               # bin centers
    yc = 0.5 * (yedges[:-1] + yedges[1:])

    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        x=xc, y=yc, z=z,
        colorscale="Blues_r",
        colorbar=dict(
            title=dict(text="pixel count"),
            tickvals=[0, 1, 2, 3],                      # log10 values…
            ticktext=[
                "10<sup>0</sup>", 
                "10<sup>1</sup>", 
                "10<sup>2</sup>", 
                "10<sup>3</sup>"],       # …shown as real counts
        ),
        hovertemplate=
        """ 
        Pixel Count: 10<sup>%{z:.1f}</sup><br>
        NDVI: %{x:.2f}<br>
        LST: %{y:.1f}°C<extra></extra>
        """,
    ))

    x = np.linspace(0,1, 100)
    fig.add_trace(go.Scatter(
        x=x, y=slope * x + intercept, mode="lines",
        line=dict(color="crimson", width=2, dash="dash"),
        name=f"fit (r = {pearson:.2f})",
    ))

    fig.update_layout(
        margin=dict(t=50, b=50, l=60, r=20),
        title=dict(text=f"Greener blocks stay cooler — {slope / 10:.2f} °C per 0.1 NDVI"),
        xaxis_title="NDVI (vegetation)",
        yaxis_title="LST (°C)",
        legend=dict(x=0.98, y=0.98, xanchor="right", yanchor="top"),
        template="plotly_white",
    )

    return fig

def make_inequality_scatter(gdf_residential, gdf):

    all_boros = gdf_residential['borocode'].unique()
    fig = go.Figure()
    for boro in all_boros:
        gdf_nb = gdf_residential.loc[gdf_residential['borocode'] == boro]
        fig.add_trace(go.Scatter(
            x = gdf_nb['lst_std'],
            y = gdf_nb['lst_mean'],
            mode = 'markers',
            # marker=dict(
            #     color=px_colorscale[boro-1],
            #     size=(gdf_nb['ndvi_mean'].astype(int)+1)*8, 
            #             ),
            showlegend=True,
            name = gdf_nb['boroname'].iloc[0]
        ))

    fig.add_vline(
        x=gdf['lst_std'].median(),
        annotation_text="LST std median",
        annotation_position="top",)
    fig.add_hline(
        y=gdf['lst_mean'].mean(),
        annotation_text="mean City LST",
        annotation_position="left",)

    return fig

def make_ranking_bar(df_ranking, value_col="lst_mean", label_col="ntaname",
                     colorscale="YlOrRd", legend_name="Mean LST (°C)",
                     title="Hottest & coolest residential neighborhoods"):
    """Ranked horizontal bar of neighborhoods by a metric.
    """
    df = df_ranking.sort_values(value_col)
    color_max = df[value_col].max() +5

    fig = go.Figure(go.Bar(
        x=df[value_col],
        y=df[label_col],
        orientation="h",
        marker=dict(
            color=df[value_col],
            colorscale=colorscale,
            cmin=20,
            cmax=color_max,
            showscale=False
        ),
        texttemplate="%{x:.1f} °C",
        textposition="outside",
        cliponaxis=False,
        customdata=df[["boroname", "ndvi_mean", "ntatype_name"]],
        hovertemplate=(
            "<b>%{y}</b> (%{customdata[0]})<br>"
            "Type: %{customdata[2]}<br>"
            "%{x:.1f}°C<br>"
            "NDVI: %{customdata[1]:.2f}<extra></extra>"
        ),
    ))

    n = len(df)
    fig.update_layout(
        margin=dict(t=50, b=40, l=10, r=20),
        title=dict(text=title),
        xaxis_title=legend_name,
        yaxis_title=None,
        template="plotly_white",
        bargap=0.5, 
        barcornerradius=10,
    )
    fig.update_xaxes(range=[20, color_max])

    return fig

def make_demographics_map(gdf, column):
    opt = DEMO_COLOR_OPTIONS[column]
    gdf_json = gdf.set_index("nb_id").__geo_interface__
    fig = go.Figure(go.Choroplethmap(
        geojson=gdf_json,
        locations=gdf["nb_id"],
        featureidkey="id",
        z=gdf[column],
        colorscale=opt["colorscale"],
        zmin=opt["zmin"], zmax=opt["zmax"],
        marker_line_color="white",
        marker_line_width=0.5,
        marker_opacity=0.8,
        colorbar=dict(title=dict(text=opt["legend"])),
        customdata=gdf[["ntaname", "boroname", column]],
        hovertemplate=(
            "<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
            f"{opt['label']}: %{{customdata[2]:.1f}}%<extra></extra>"
        ),
    ))
    fig.update_layout(
        margin=dict(t=30, b=0, l=0, r=0),
        title=dict(text=opt["label"], x=0.5, xanchor="center"),
        map=dict(center=dict(lat=40.70, lon=-73.95), zoom=9),
    )
    return fig


def make_predominant_map(gdf):
    n = len(DEMO_GROUPS)
    group_to_int = {g: i for i, g in enumerate(DEMO_GROUPS)}
    colors = list(DEMO_GROUP_COLORS.values())

    colorscale = []
    for i, c in enumerate(colors):
        colorscale += [[i / n, c], [(i + 1) / n, c]]

    z = gdf["predominant_group"].map(group_to_int)
    gdf_json = gdf.set_index("nb_id").__geo_interface__

    fig = go.Figure(go.Choroplethmap(
        geojson=gdf_json,
        locations=gdf["nb_id"],
        featureidkey="id",
        z=z,
        colorscale=colorscale,
        zmin=0, zmax=n - 1,
        showscale=False,
        marker_line_color="white",
        marker_line_width=0.5,
        marker_opacity=0.8,
        customdata=gdf[["ntaname", "boroname", "predominant_group"]],
        hovertemplate=(
            "<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
            "Predominant: %{customdata[2]}<extra></extra>"
        ),
    ))

    for group, color in DEMO_GROUP_COLORS.items():
        fig.add_trace(go.Scattermap(
            lat=[None], lon=[None],
            mode="markers",
            marker=dict(size=12, color=color),
            name=group.capitalize(),
            showlegend=True,
        ))

    fig.update_layout(
        margin=dict(t=30, b=0, l=0, r=0),
        title=dict(text="Predominant ethnic group by neighborhood", x=0.5, xanchor="center"),
        map=dict(center=dict(lat=40.70, lon=-73.95), zoom=9),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"),
    )
    return fig