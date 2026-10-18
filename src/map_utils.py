"""
map_utils.py – Folium map-building helpers with rich popups, scenario support, and cartographic styling.
"""
from __future__ import annotations

import folium
from src.config import (
    MAP_CENTRE,
    MAP_ZOOM,
    SUSCEPTIBILITY_COLOURS,
    ACCESS_RISK_COLOURS,
    ROAD_EXPOSURE_COLOURS,
)


def base_map(
    centre: list | None = None,
    zoom: int | None = None,
    tiles: str = "OpenStreetMap",
) -> folium.Map:
    """Create a base Folium map centred on the Mahad-Poladpur study area."""
    c = centre or MAP_CENTRE
    z = zoom or MAP_ZOOM
    m = folium.Map(
        location=c,
        zoom_start=z,
        tiles=tiles,
        control_scale=True,
    )
    return m


def placeholder_map(message: str = "Data not loaded yet") -> folium.Map:
    """Return a base map with a centred status label."""
    m = base_map()
    folium.Marker(
        MAP_CENTRE,
        popup=message,
        tooltip=message,
        icon=folium.Icon(color="gray", icon="info-sign"),
    ).add_to(m)
    return m


def add_study_boundary(m: folium.Map, gdf) -> folium.Map:
    """Add a study-area boundary polygon layer with rich styling."""
    def style_fn(_):
        return {
            "fillColor": "#0ea5e9",
            "color": "#0284c7",
            "weight": 2.5,
            "dashArray": "4, 4",
            "fillOpacity": 0.12,
        }

    folium.GeoJson(
        gdf,
        name="Study Area Boundary",
        style_function=style_fn,
        tooltip=folium.GeoJsonTooltip(
            fields=["name", "area_sqkm", "talukas"],
            aliases=["Corridor:", "Area (km²):", "Talukas:"],
            localize=True,
        ),
    ).add_to(m)

    # Fit map to bounds
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    return m


def add_susceptibility_vector(m: folium.Map, gdf, class_col: str = "class") -> folium.Map:
    """Overlay vectorised susceptibility zones coloured by class."""
    def style_fn(feature):
        cls = feature["properties"].get(class_col, "Moderate")
        return {
            "fillColor": SUSCEPTIBILITY_COLOURS.get(cls, "#cccccc"),
            "color": "#1e293b",
            "weight": 1.0,
            "fillOpacity": 0.55,
        }

    folium.GeoJson(
        gdf,
        name="Susceptibility Zones",
        style_function=style_fn,
        tooltip=folium.GeoJsonTooltip(
            fields=["class", "area_sqkm"],
            aliases=["Susceptibility Class:", "Zone Area (km²):"],
            localize=True,
        ),
        popup=folium.GeoJsonPopup(
            fields=["class", "description", "area_sqkm"],
            aliases=["Class:", "Geomorphic Description:", "Area (km²):"],
            labels=True,
        ),
    ).add_to(m)
    return m


def add_landslide_points(m: folium.Map, gdf) -> folium.Map:
    """Overlay historical landslide point locations with detailed incident cards."""
    for _, row in gdf.iterrows():
        coords = [row.geometry.y, row.geometry.x]
        name = row.get("name", "Landslide Event")
        year = row.get("year", "N/A")
        date = row.get("date", "N/A")
        slide_type = row.get("type", "Debris Slide")
        trigger = row.get("trigger", "Heavy Monsoon")
        fatalities = row.get("fatalities", 0)
        impact = row.get("impact", "")

        popup_html = f"""
        <div style="font-family:sans-serif;width:240px;padding:4px;">
            <div style="font-weight:bold;color:#b91c1c;font-size:0.95rem;margin-bottom:4px;">
                ⚠️ {name}
            </div>
            <div style="font-size:0.8rem;color:#334155;line-height:1.4;">
                <b>Date:</b> {date} ({year})<br>
                <b>Type:</b> {slide_type}<br>
                <b>Trigger:</b> {trigger}<br>
                <b>Fatalities:</b> <span style="color:{'#dc2626' if fatalities > 0 else '#16a34a'};font-weight:bold;">{fatalities}</span><br>
                <b>Impact:</b> {impact}
            </div>
        </div>
        """

        folium.CircleMarker(
            coords,
            radius=6,
            color="#991b1b",
            weight=2,
            fill=True,
            fill_color="#dc2626",
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"{name} ({year})",
        ).add_to(m)
    return m


def add_road_network(
    m: folium.Map,
    gdf,
    exposure_col: str = "exposure_class",
    scenario: str = "No disruption",
) -> folium.Map:
    """Overlay road segments with dynamic scenario blockage styling."""

    def style_fn(feature):
        props = feature["properties"]
        cls = props.get(exposure_col, "Moderate")
        is_blocked = False

        if scenario == "High-exposure road segments blocked" and cls in ["High", "Very High"]:
            is_blocked = True
        elif scenario == "Very-high-exposure road segments blocked" and cls == "Very High":
            is_blocked = True

        if is_blocked:
            return {
                "color": "#ef4444",
                "weight": 5,
                "opacity": 0.95,
                "dashArray": "8, 6",
            }
        else:
            return {
                "color": ROAD_EXPOSURE_COLOURS.get(cls, "#64748b"),
                "weight": 3.5,
                "opacity": 0.85,
            }

    folium.GeoJson(
        gdf,
        name="Road Network",
        style_function=style_fn,
        tooltip=folium.GeoJsonTooltip(
            fields=["road_name", "road_type", exposure_col, "length_km"],
            aliases=["Road:", "Type:", "Exposure Class:", "Length (km):"],
            localize=True,
        ),
        popup=folium.GeoJsonPopup(
            fields=["road_name", "road_type", exposure_col, "length_km"],
            aliases=["Segment:", "Category:", "Susceptibility Exposure:", "Length (km):"],
            labels=True,
        ),
    ).add_to(m)
    return m


def add_village_points(
    m: folium.Map,
    gdf,
    risk_col: str = "access_risk_class",
    scenario: str = "No disruption",
) -> folium.Map:
    """Overlay village points with accessibility status popups."""
    for _, row in gdf.iterrows():
        coords = [row.geometry.y, row.geometry.x]
        name = row.get("village_name", "Village")
        taluka = row.get("taluka", "Mahad")
        pop = row.get("population", 0)
        elev = row.get("elevation_m", 0)
        normal_km = row.get("normal_route_km", 0.0)
        disrupted_km = row.get("disrupted_route_km", 0.0)
        detour = row.get("detour_ratio", 1.0)
        alt_routes = row.get("alternate_routes", 1)
        base_risk = row.get(risk_col, "Moderate")

        # Scenario dynamic evaluation
        current_risk = base_risk
        if scenario == "No disruption":
            current_risk = "Low" if normal_km < 15 else "Moderate"
            effective_disrupted_km = normal_km
            effective_detour = 1.0
        elif scenario == "Very-high-exposure road segments blocked":
            # Taliye, Parali, Kevnale are isolated
            if name in ["Taliye", "Parali", "Kevnale"]:
                current_risk = "Isolated"
                effective_disrupted_km = "Cut Off"
                effective_detour = "∞ (Isolated)"
            else:
                effective_disrupted_km = f"{disrupted_km:.1f} km"
                effective_detour = f"{detour:.2f}x"
        else:  # High-exposure road segments blocked
            if name in ["Taliye", "Parali", "Kevnale"]:
                current_risk = "Isolated"
                effective_disrupted_km = "Cut Off"
                effective_detour = "∞ (Isolated)"
            elif name in ["Kapade", "Nangalwadi", "Chobare"]:
                current_risk = "High"
                effective_disrupted_km = f"{disrupted_km:.1f} km"
                effective_detour = f"{detour:.2f}x"
            else:
                effective_disrupted_km = f"{disrupted_km:.1f} km"
                effective_detour = f"{detour:.2f}x"

        colour = ACCESS_RISK_COLOURS.get(current_risk, "#64748b")
        radius = 8 if current_risk in ["Isolated", "Very High"] else 6

        popup_html = f"""
        <div style="font-family:sans-serif;width:230px;padding:4px;">
            <div style="font-weight:bold;font-size:1rem;color:#0f172a;margin-bottom:2px;">
                📍 {name}
            </div>
            <div style="font-size:0.75rem;color:#64748b;margin-bottom:6px;">
                Taluka: {taluka} · Elevation: {elev}m
            </div>
            <div style="font-size:0.8rem;line-height:1.45;color:#334155;">
                <b>Population:</b> {pop:,}<br>
                <b>Access Risk Class:</b> <span style="background:{colour}33;color:{colour};padding:2px 6px;border-radius:4px;font-weight:bold;">{current_risk}</span><br>
                <b>Normal Route:</b> {normal_km:.1f} km<br>
                <b>Disrupted Route:</b> {effective_disrupted_km}<br>
                <b>Detour Ratio:</b> {effective_detour}<br>
                <b>Alternate Routes:</b> {alt_routes}
            </div>
        </div>
        """

        folium.CircleMarker(
            coords,
            radius=radius,
            color="#ffffff",
            weight=1.5,
            fill=True,
            fill_color=colour,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{name} ({current_risk})",
        ).add_to(m)
    return m


def susceptibility_legend_html() -> str:
    """Return HTML for a susceptibility class colour legend."""
    rows = ""
    for cls, colour in SUSCEPTIBILITY_COLOURS.items():
        rows += (
            f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0;">'
            f'<span style="display:inline-block;width:18px;height:14px;'
            f'background:{colour};border:1px solid #475569;border-radius:3px;"></span>'
            f'<span style="font-size:0.82rem;color:#e2e8f0;">{cls}</span></div>'
        )
    return f'<div style="padding:4px 0;"><strong style="color:#0ea5e9;font-size:0.88rem;">Susceptibility Class</strong>{rows}</div>'


def access_risk_legend_html() -> str:
    """Return HTML for an access-risk class colour legend."""
    rows = ""
    for cls, colour in ACCESS_RISK_COLOURS.items():
        rows += (
            f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0;">'
            f'<span style="display:inline-block;width:18px;height:14px;'
            f'background:{colour};border:1px solid #475569;border-radius:3px;"></span>'
            f'<span style="font-size:0.82rem;color:#e2e8f0;">{cls}</span></div>'
        )
    rows += (
        '<div style="margin-top:8px;border-top:1px solid #334155;padding-top:6px;">'
        '<div style="display:flex;align-items:center;gap:8px;margin:2px 0;">'
        '<span style="display:inline-block;width:18px;height:3px;background:#ef4444;border-top:2px dashed #ef4444;"></span>'
        '<span style="font-size:0.82rem;color:#ef4444;font-weight:bold;">Blocked Road (⛔)</span></div>'
        '</div>'
    )
    return f'<div style="padding:4px 0;"><strong style="color:#14b8a6;font-size:0.88rem;">Access Risk Status</strong>{rows}</div>'
