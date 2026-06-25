NTA_MAPPING_GRAPH = {
    "Downtown Brooklyn-DUMBO-Boerum Hill" : "Downtown Brooklyn-DUMBO",
    "Highland Park-Cypress Hills Cemeteries (South)" : "Highland Park (South)",
    "Carroll Gardens-Cobble Hill-Gowanus-Red Hook" : "Carroll Gardens",
    "Prospect Lefferts Gardens-Wingate" : "Prospect Lefferts Gardens",
    "Sunset Park (East)-Borough Park (West)" : "Sunset Park (East)",
    "Flatbush (West)-Ditmas Park-Parkville" : "Flatbush (West)",
    "Sheepshead Bay-Manhattan Beach-Gerritsen Beach" : "Sheepshead Bay",
    "Marine Park-Mill Basin-Bergen Beach" : "Marine Park-Mill Basin",
    "Barren Island-Floyd Bennett Field" : "Barren Island",
    "Claremont Village-Claremont (East)" : "Claremont East",
    "Yankee Stadium-Macombs Dam Park" : "Yankee Stadium",
    "University Heights (South)-Morris Heights" : "University Heights (South)",
    "University Heights (North)-Fordham" : "University Heights (North)",
    "Kingsbridge Heights-Van Cortlandt Village" : "Kingsbridge Heights",
    "Pelham Bay-Country Club-City Island" : "Pelham Bay",
    "Ferry Point Park-St. Raymond Cemetery" : "Ferry Point Park",
    "Eastchester-Edenwald-Baychester" : "Eastchester-Edenwald",
    "Financial District-Battery Park City" : "FiDi-Battery Park",
    "The Battery-Governors Island-Ellis Island-Liberty Island" : "Battery-Governors Island",
    "SoHo-Little Italy-Hudson Square" : "SoHo-Little Italy-Hudson Sq",
    "Midtown South-Flatiron-Union Square" : "Flatiron-Union Square",
    "Stuyvesant Town-Peter Cooper Village" : "Stuyvesant Town",
    "Upper West Side-Manhattan Valley" : "Upper West Side",
    "Upper East Side-Lenox Hill-Roosevelt Island" : "Upper East Side",
    "Astoria (North)-Ditmars-Steinway" : "Astoria (North)",
    "Astoria (East)-Woodside (North)" : "Astoria (East)",
    "Queensbridge-Ravenswood-Dutch Kills" : "Queensbridge",
    "Calvary & Mount Zion Cemeteries" : "Calvary - Mt. Zion Cemeteries",
    "Mount Olivet & All Faiths Cemeteries" : "Mt. Olivet Cemetery",
    "Highland Park-Cypress Hills Cemeteries (North)" : "Highland Park (North)",
    "Mount Hebron & Cedar Grove Cemeteries" : "Mt. Hebron Cemetery",
    "Springfield Gardens (North)-Rochdale Village" : "Springfield Gardens (North)",
    "Glen Oaks-Floral Park-New Hyde Park" : "Glen Oaks-Floral Park",
    "Springfield Gardens (South)-Brookville" : "Springfield Gardens (South)",
    "Rockaway Beach-Arverne-Edgemere" : "Rockaway Beach",
    "Breezy Point-Belle Harbor-Rockaway Park-Broad Channel" : "Breezy Point-Belle Harbor",
    "John F. Kennedy International Airport" : "JFK Airport",
    "Jacob Riis Park-Fort Tilden-Breezy Point Tip" : "Jacob Riis Park",
    "Tompkinsville-Stapleton-Clifton-Fox Hills" : "Tompkinsville-Stapleton",
    "West New Brighton-Silver Lake-Grymes Hill" : "West New Brighton",
    "Mariner's Harbor-Arlington-Graniteville" : "Mariner's Harbor-Arlington",
    "Grasmere-Arrochar-South Beach-Dongan Hills" : "Grasmere-Arrochar",
    "Todt Hill-Emerson Hill-Lighthouse Hill-Manor Heights" : "Todt Hill",
    "New Springville-Willowbrook-Bulls Head-Travis" : "New Springville",
    "Annadale-Huguenot-Prince's Bay-Woodrow" : "Annadale-Huguenot",
}


OVERVIEW_DESCRIPTION="""
A pixel-by-pixel reading of land-surface temperature (LST) against vegetation (NDVI) across New York City 
neighborhoods, from Landsat 8 thermal imagery on clear summer days.
"""

SECTION_LST_NDVI_MAP = """ 
*(Left) Residential neighborhoods colored by deviation from city-mean surface temperature.* 
*(Right) All neighborhoods colored by vegetation index (NDVI, Higher is Greener)*.

- Residential areas are cooler when they are near parks and/or water areas. 
- Hottest residential areas cluster in southeast Queens, where NDVI is lowest

The pattern is clear: **greener neighborhoods are cooler.**
"""

SECTION_LST_NDVI_CORR = """ 
Across all land pixels the relationship is strong: ~ -0.9 °C per 0.1 NDVI. Filter to residential 
areas only and the correlation drops sharply (r ≈ 0.26).

**Greenery alone cannot explain the heat.** Building density, waste heat from AC systems, 
and absence of waterfront/river all contribute.
"""

SECTION_RANKED_BAR = """ 
Parks are the coolest places and residential areas the hottest after airports. Within residential 
neighborhoods, **Queens dominates the top** of the list. 

FiDi ranks among the coolest even with an NDVI of 0.19, it's surrounded by water on three sides,
highlightig that NDVI is only one cooling driver.
"""

SECTION_INEQUALITY_SCATTER = """ 
The scatter plot reveals who gets relief and who does not. 
- **Top-left quadrant** (hot, low variability): neighborhoods that are uniformly hot with no cool refuge (Queens, Brooklyn). 
- **Right side** (high variability): neighborhoods where people can find relief near waterfronts/parks (Staten Island, Manhattan). 
- The population at the highest risk live in hot and uniform environment.
"""

SECTION_DEMOGRAPHICS = """ 
Overlay demographics with neighborhoods:
-  The predominantly **Hispanic and Black neighborhoods** in the Bronx and Queens align with the hottest and lowest-NDVI residential areas.
- Meanwhile, the coolest residential neighborhoods (Staten Island, Manhattan) are predominantly White. 
- The heat burden in New York is unevenly distributed, and it broadly tracks with the city's racial and socioeconomic geography.
"""