"""
data_loader.py – Safe data-loading utilities.

Every loader returns (data | None, status_message).
The dashboard never crashes on missing data; it shows a clear status message.
"""
from __future__ import annotations

import pathlib
from typing import Optional, Tuple

import pandas as pd

try:
    import geopandas as gpd
except ImportError:
    gpd = None  # type: ignore

try:
    import rasterio
except ImportError:
    rasterio = None  # type: ignore

from src.config import EXPECTED_FILES


# ── Helpers ──────────────────────────────────────────────────────────────────

def _file_exists(key: str) -> Tuple[bool, pathlib.Path]:
    """Check if an expected processed file exists."""
    path = EXPECTED_FILES.get(key)
    if path is None:
        return False, pathlib.Path("")
    return path.exists(), path


def check_all_files() -> dict[str, dict]:
    """Return a dict keyed by file label with existence & path info."""
    report: dict[str, dict] = {}
    for key, path in EXPECTED_FILES.items():
        report[key] = {
            "path": str(path),
            "filename": path.name,
            "exists": path.exists(),
        }
    return report


# ── GeoJSON loaders ──────────────────────────────────────────────────────────

def load_geojson(key: str) -> Tuple[Optional["gpd.GeoDataFrame"], str]:
    """Load a GeoJSON file registered in EXPECTED_FILES."""
    if gpd is None:
        return None, "⚠️ GeoPandas is not installed."
    exists, path = _file_exists(key)
    if not exists:
        return None, f"📂 **Data not loaded yet** – `{path.name}` not found in `data/processed/`."
    try:
        gdf = gpd.read_file(path)
        if gdf.empty:
            return None, f"⚠️ `{path.name}` is empty (0 features)."
        return gdf, f"✅ Loaded `{path.name}` ({len(gdf)} features)."
    except Exception as exc:
        return None, f"❌ Error reading `{path.name}`: {exc}"


# ── Raster loader ────────────────────────────────────────────────────────────

def load_raster(key: str = "susceptibility_raster"):
    """Load a GeoTIFF and return (dataset, array, status_message).

    Returns (None, None, msg) on failure.
    """
    if rasterio is None:
        return None, None, "⚠️ Rasterio is not installed."
    exists, path = _file_exists(key)
    if not exists:
        return None, None, f"📂 **Data not loaded yet** – `{path.name}` not found in `data/processed/`."
    try:
        ds = rasterio.open(path)
        arr = ds.read(1)
        return ds, arr, f"✅ Loaded `{path.name}` ({arr.shape[1]}×{arr.shape[0]} px)."
    except Exception as exc:
        return None, None, f"❌ Error reading `{path.name}`: {exc}"


# ── CSV loaders ──────────────────────────────────────────────────────────────

def load_csv(key: str) -> Tuple[Optional[pd.DataFrame], str]:
    """Load a CSV file registered in EXPECTED_FILES."""
    exists, path = _file_exists(key)
    if not exists:
        return None, f"📂 **Data not loaded yet** – `{path.name}` not found in `data/processed/`."
    try:
        df = pd.read_csv(path)
        if df.empty:
            return None, f"⚠️ `{path.name}` is empty (0 rows)."
        return df, f"✅ Loaded `{path.name}` ({len(df)} rows)."
    except Exception as exc:
        return None, f"❌ Error reading `{path.name}`: {exc}"
