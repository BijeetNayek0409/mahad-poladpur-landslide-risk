"""
config.py – Colour palettes, file paths, and project constants.
"""
import pathlib

# ── Project root ──────────────────────────────────────────────────────────────
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent

# ── Data paths ────────────────────────────────────────────────────────────────
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS_MAPS = PROJECT_ROOT / "outputs" / "maps"
OUTPUTS_TABLES = PROJECT_ROOT / "outputs" / "tables"

# ── Expected processed files ─────────────────────────────────────────────────
EXPECTED_FILES = {
    "study_area_boundary": DATA_PROCESSED / "study_area_boundary.geojson",
    "susceptibility_raster": DATA_PROCESSED / "susceptibility_raster.tif",
    "susceptibility_vector": DATA_PROCESSED / "susceptibility_vector.geojson",
    "landslide_inventory": DATA_PROCESSED / "landslide_inventory.geojson",
    "road_network": DATA_PROCESSED / "road_network.geojson",
    "villages": DATA_PROCESSED / "villages.geojson",
    "village_access_table": DATA_PROCESSED / "village_access_table.csv",
    "ahp_weights": DATA_PROCESSED / "ahp_weights.csv",
    "validation_results": DATA_PROCESSED / "validation_results.csv",
}

# ── Susceptibility class definitions ─────────────────────────────────────────
SUSCEPTIBILITY_CLASSES = {
    1: "Very Low",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Very High",
}

SUSCEPTIBILITY_COLOURS = {
    "Very Low": "#2b83ba",
    "Low": "#abdda4",
    "Moderate": "#ffffbf",
    "High": "#fdae61",
    "Very High": "#d7191c",
}

# ── Access-risk class definitions ─────────────────────────────────────────────
ACCESS_RISK_CLASSES = ["Low", "Moderate", "High", "Very High", "Isolated"]

ACCESS_RISK_COLOURS = {
    "Low": "#2b83ba",
    "Moderate": "#abdda4",
    "High": "#fdae61",
    "Very High": "#d7191c",
    "Isolated": "#7b3294",
}

# ── Road exposure class definitions ──────────────────────────────────────────
ROAD_EXPOSURE_COLOURS = {
    "Very Low": "#2b83ba",
    "Low": "#abdda4",
    "Moderate": "#ffffbf",
    "High": "#fdae61",
    "Very High": "#d7191c",
}

# ── Dashboard colour palette (CSS custom properties) ─────────────────────────
PALETTE = {
    "bg_dark": "#0e1117",
    "bg_card": "#1a1f2e",
    "primary": "#0ea5e9",       # sky-500  (blue)
    "secondary": "#14b8a6",     # teal-500
    "accent": "#f97316",        # orange-500
    "text": "#e2e8f0",
    "text_muted": "#94a3b8",
    "border": "#334155",
    "success": "#22c55e",
    "warning": "#eab308",
    "danger": "#ef4444",
}

# ── Map defaults ──────────────────────────────────────────────────────────────
# Approximate centre of the Mahad–Poladpur corridor
MAP_CENTRE = [18.08, 73.45]
MAP_ZOOM = 11

# ── Disruption scenarios ─────────────────────────────────────────────────────
SCENARIOS = [
    "No disruption",
    "High-exposure road segments blocked",
    "Very-high-exposure road segments blocked",
]

# ── Dataset inventory (processed project metadata) ───────────────────────────
DATASET_INVENTORY = [
    {
        "Dataset": "Digital Elevation Model (DEM)",
        "Source": "USGS SRTM 1 Arc-Second Global",
        "Date": "2020 (Rev 2021)",
        "Resolution": "30 m (1 arc-sec)",
        "Coverage": "Mahad–Poladpur Corridor (542.8 km²)",
        "Processing Status": "✅ Processed",
        "Limitations": "Hydro-conditioned; 30m resolution smooths micro-gullies (<15m width)",
    },
    {
        "Dataset": "Monsoon Rainfall Records",
        "Source": "IMD Pune High-Res Gridded Precipitation",
        "Date": "2018–2023 (Monsoon Jun–Sep)",
        "Resolution": "0.25° × 0.25° (gridded)",
        "Coverage": "Raigad District & Western Ghats",
        "Processing Status": "✅ Processed",
        "Limitations": "Downscaled via IDW with local rain-gauge network (Mahad, Poladpur)",
    },
    {
        "Dataset": "Landslide Inventory",
        "Source": "GSI National Landslide Susceptibility Mapping & District Cell",
        "Date": "2018–2022 (Verified Post-2021)",
        "Resolution": "Point & Polygon GPS locations",
        "Coverage": "Study Corridor & Ghat Sections",
        "Processing Status": "✅ Processed",
        "Limitations": "15 major verified events catalogued; minor road cuts may be under-reported",
    },
    {
        "Dataset": "Road Network",
        "Source": "Maharashtra PWD & OpenStreetMap (OSM)",
        "Date": "2023 (Road Asset Inventory)",
        "Resolution": "Vector LineStrings (1:10,000 scale)",
        "Coverage": "NH-66, SH-72, SH-96 & Rural Arterials",
        "Processing Status": "✅ Processed",
        "Limitations": "Topology cleansed; culvert & ghat hairpins mapped with PWD road markers",
    },
    {
        "Dataset": "Village Settlements",
        "Source": "Census of India & Survey of India Revenue Settlements",
        "Date": "2011 (Updated 2021)",
        "Resolution": "Point Centroids & Habitation Polygons",
        "Coverage": "14 Monitored Hubs & Villages",
        "Processing Status": "✅ Processed",
        "Limitations": "Population matched to 2011 census with 2021 electoral revision estimates",
    },
    {
        "Dataset": "Land Use / Land Cover (LULC)",
        "Source": "ISRO Bhuvan High-Resolution LULC",
        "Date": "2020",
        "Resolution": "30 m Multi-spectral",
        "Coverage": "Mahad–Poladpur Catchment",
        "Processing Status": "✅ Processed",
        "Limitations": "Reclassified into 5 hydrologic & slope stabilization classes",
    },
    {
        "Dataset": "Geology / Lithology & Soil",
        "Source": "GSI District Resource Map & NBSS&LUP Soil Series",
        "Date": "2019",
        "Resolution": "1:50,000 Scale",
        "Coverage": "Southern Raigad Deccan Basalt Province",
        "Processing Status": "✅ Processed",
        "Limitations": "Compound Deccan lava flows overlain by weathered laterite cap",
    },
]

# ── AHP factor list ──────────────────────────────────────────────────────────
AHP_FACTORS = [
    {
        "Factor": "Slope",
        "Description": "Terrain gradient derived from DEM",
        "Relevance": "Steeper slopes increase gravitational driving forces on potentially unstable material.",
    },
    {
        "Factor": "Rainfall Intensity",
        "Description": "Monsoon cumulative / intensity rainfall grids",
        "Relevance": "Rainfall is the primary triggering mechanism for shallow landslides in the Western Ghats.",
    },
    {
        "Factor": "Drainage Density",
        "Description": "Stream network density per unit area",
        "Relevance": "High drainage density indicates rapid run-off and potential pore-pressure build-up.",
    },
    {
        "Factor": "Curvature",
        "Description": "Plan / profile curvature from DEM",
        "Relevance": "Concave surfaces concentrate water flow, increasing saturation potential.",
    },
    {
        "Factor": "Land Use / Land Cover",
        "Description": "Classified land-cover map",
        "Relevance": "Barren or deforested slopes have reduced root cohesion and higher erosion susceptibility.",
    },
    {
        "Factor": "Geology / Soil",
        "Description": "Lithological and soil-type maps",
        "Relevance": "Residual soils over weathered basalt are common failure-prone substrates in the Deccan Traps.",
    },
]
