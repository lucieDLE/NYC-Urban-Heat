DEMO_GROUP_COLORS = {
    "hispanic":           "#e6550d",  # Oranges mid
    "white":              "#756bb1",  # Purples mid
    "black":              "#3182bd",  # Blues mid
    "asian":              "#31a354",  # Greens mid
}
DEMO_GROUPS = list(DEMO_GROUP_COLORS.keys())

BORO_COLORS = {
    "Manhattan":    "#D55E00",
    "Brooklyn":     "#4477AA",
    "Queens":       "#228833",
    "Bronx":    "#9467BD",
    "Staten Island":"#D62728",
}

COLOR_OPTIONS = {
    "lst_mean_dev": {
        "label": "Deviation from City-Mean surface temperature",
        "legend": "LST (°C)",
        "colorscale": "RdYlBu_r",
        "zmin": None, "zmax": None,
        "colorline": "black",

    },
    "ndvi_mean": {
        "label": "Vegetation (NDVI)",
        "legend": "NDVI",
        "colorscale": "RdYlGn",
        "zmin": -1, "zmax":1, 
        "colorline": "green",
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
