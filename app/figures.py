
COLS_DISPLAY= [
    "ntaname", "boroname", 
    "ntatype_name",
    "lst_mean", "lst_std", 
    "lst_min", "lst_max", 
    "ndvi_mean", "ndvi_std",
    "ndvi_min", "ndvi_max",
    ]

def make_cloropleth_map(gdf, column_name):

    gdf_json = gdf.set_index("nb_id").__geo_interface__

    fig = go.Figure(data=go.Choroplethmap(
        geojson=gdf_json,
        locations=gdf["nb_id"],
        featureidkey="id",
        z=gdf[column_name],
        colorscale="RdYlGn",
        zmin=-1, zmax=1,            # NDVI range for built-up NYC (tweak to taste)
        marker_line_color="green",
        marker_line_width=0.5,
        marker_opacity=0.7,
        colorbar=dict(title=dict(text="NDVI")),
        customdata=gdf[COLS_DISPLAY],
        hovertemplate=(
            "<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
            "type : %{customdata[2]}<br> <br>"

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
        margin=dict(t=0, b=0, l=0, r=0),
        map=dict(
            style="open-street-map",
            center=dict(lat=40.70, lon=-73.95),
            zoom=9,
        ),
    )

    return fig
