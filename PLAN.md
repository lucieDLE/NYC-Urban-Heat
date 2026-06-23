Progress So Far

[x] LST loaded, scale factor applied, cloud masked, plotted
[x] Neighborhoods and parks loaded and plotted together
[x] Reproject vector to match raster CRS (EPSG:32618)
[x] Clip raster to NYC extent
[x] Compute NDVI from B4/B5
[x] Pixel-level analysis (LST vs NDVI scatter + correlation)
[x] Neighborhood-level choropleth (mean temp per neighborhood)

[x] Test if correlation map plot per neighborhood is meaningful (No)
[ ] Add Water (if possible from satellite) into cooling analysis
[ ] Final visualization (Folium interactive map + Plotly charts)
[ ] Identify neighborhoods that are both hot, low-green, and densely populated (highest heat risk)
[ ] Population-weighted mean LST per demographic group: Σ(group_count×lst_mean)/Σ(group_count) → headline bar chart
[ ] Regression LST ~ NDVI + water + %group 
[ ] Income ?