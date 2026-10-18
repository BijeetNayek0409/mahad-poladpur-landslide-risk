# Mahad-Poladpur Landslide and Village Access Risk Dashboard

A **decision-support and scenario-analysis tool** for exploring monsoon landslide
susceptibility and road-access risk for villages in the Mahad–Poladpur corridor,
Raigad District, Maharashtra, India.

> **Disclaimer:** This dashboard is a research and educational tool for spatial
> analysis. It is **not** an operational landslide prediction, early-warning, or
> forecasting system. Results depend entirely on input data quality and the
> analytical assumptions documented in the *Method, Validation & Limitations* tab.

---

## Quick Start

```bash
# 1. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

---

## Directory Structure

```
mahad-poladpur-landslide-risk/
├── app.py                  # Main Streamlit application (multi-page tabs)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── data/
│   ├── raw/                # Original, unprocessed datasets (DEM, shapefiles, etc.)
│   └── processed/          # Analysis-ready layers produced by GIS workflows
├── outputs/
│   ├── maps/               # Exported map images / HTML maps
│   └── tables/             # Exported CSV / Excel result tables
└── src/
    ├── __init__.py
    ├── data_loader.py      # Functions to safely load & validate project data
    ├── map_utils.py        # Folium / map-building helpers
    └── config.py           # Colour palettes, constants, file-path conventions
```

---

## Expected Processed Data Files

Place the following files in `data/processed/` once your GIS analysis is
complete. The dashboard detects their presence automatically.

| File | Format | Description |
|------|--------|-------------|
| `study_area_boundary.geojson` | GeoJSON (polygon) | Boundary of the Mahad–Poladpur study corridor |
| `susceptibility_raster.tif` | GeoTIFF (5 classes, 1–5) | Five-class landslide susceptibility raster |
| `susceptibility_vector.geojson` | GeoJSON (polygon) | Vectorised susceptibility zones (optional) |
| `landslide_inventory.geojson` | GeoJSON (point) | Verified historical landslide locations |
| `road_network.geojson` | GeoJSON (line) | Road segments with `exposure_class` attribute |
| `villages.geojson` | GeoJSON (point) | Village locations with accessibility attributes |
| `village_access_table.csv` | CSV | Village access-risk table (see schema below) |
| `ahp_weights.csv` | CSV | AHP pair-wise comparison weights & CR |
| `validation_results.csv` | CSV | Held-out validation metrics |

### Village Access Table Schema

| Column | Type | Description |
|--------|------|-------------|
| `village_name` | str | Name of the village |
| `normal_route_km` | float | Shortest-path distance under no-disruption scenario (km) |
| `disrupted_route_km` | float | Shortest-path distance when high-exposure roads blocked (km) |
| `detour_ratio` | float | `disrupted_route_km / normal_route_km` |
| `alternate_routes` | int | Number of distinct alternate routes available |
| `access_risk_class` | str | Low / Moderate / High / Very High / Isolated |
| `notes` | str | Free-text notes |

---

## Research Limitations

1. **Landslide inventory completeness** – The inventory may under-represent
   smaller or unreported events.
2. **DEM resolution** – Derived slope / curvature accuracy depends on DEM
   spatial resolution.
3. **Rainfall resolution** – Gridded rainfall data may not capture highly
   localised orographic variation.
4. **Road-network quality** – OpenStreetMap or manually digitised roads may
   contain positional errors or missing segments.
5. **Simplified blockage scenarios** – The model assumes binary
   open/closed road segments; partial blockage is not modelled.
6. **No operational forecasting** – This tool does not ingest real-time
   weather data and must not be used for emergency response.

---

## License

This project is part of an academic research study. All data and code are
provided for educational and research purposes only.
