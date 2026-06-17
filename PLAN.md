Project: NYC Urban Heat Island Analysis
Goal: Analyze the relationship between urban vegetation and surface temperature across New York City
- identifying which neighborhoods are hottest
- where green space is lacking
- quantifying the temperature-cooling effect of vegetation.

Core Question
Do neighborhoods with more green space stay cooler in summer? Which neighborhoods are most heat-exposed?

Data
Landsat 8: Path 013 Row 032 (covers NYC) from UGSC

LC08_L2SP_013032_20250830 — Aug 2025
LC08_L2SP_013032_20230809 — Aug 2023
LC08_L2SP_013032_20220806 — Aug 2022
LC08_L2SP_013032_20190729 — Jul 2019

Each scene contains:

ST_B10.TIF — Land Surface Temperature (raw, needs scale factor)
SR_B4.TIF / SR_B5.TIF — Red/NIR bands for NDVI
QA_PIXEL.TIF — Cloud mask

Scale factors:

Temperature: raw × 0.00341802 + 149.0 - 273.15 → Celsius
Reflectance: raw × 0.0000275 + (-0.2)

Vector data (loaded, CRS: EPSG:4326)

NYC Neighborhood Tabulation Areas (NTAs)
NYC Parks polygons (via osmnx or NYC Open Data)

Raster CRS: EPSG:32618 (WGS84 UTM Zone 18N, meters)

Progress So Far

[x] LST loaded, scale factor applied, cloud masked, plotted
[x] Neighborhoods and parks loaded and plotted together
[x] Reproject vector to match raster CRS (EPSG:32618)
[x] Clip raster to NYC extent
[x] Compute NDVI from B4/B5
[x] Pixel-level analysis (LST vs NDVI scatter + correlation)
[x] Neighborhood-level choropleth (mean temp per neighborhood)

[ ] Test if correlation map plot per neighborhood is meaningful
[ ] Add Water (if possible from satellite) into cooling analysis
[ ] Final visualization (Folium interactive map + Plotly charts)
[ ] Socioeconomic analysis: overlay population density to identify neighborhoods that are both hot, low-green, AND densely populated (highest heat risk).
