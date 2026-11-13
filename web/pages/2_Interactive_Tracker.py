import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from top_model_renderer import render_top_model
from historical_river_datasets import HISTORICAL_RIVERS
import streamlit as st
import xarray as xr
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Ocean Plastic Tracker", layout="wide")

st.title("Ocean Plastic Tracker")
st.caption("Classroom prototype — OceanParcels / GLORYS12V1")

RIVERS = {
    "Pasig": ("North Pacific", 1, 6.4),
    "Klang": ("Indian Ocean", 2, 1.3),
    "Ulhas": ("Indian Ocean", 3, 1.3),
    "Tullahan": ("North Pacific", 4, 1.3),
    "Meycauayan": ("North Pacific", 5, 1.2),
    "Pampanga": ("North Pacific", 6, 0.95),
    "Libmanan": ("North Pacific", 7, 0.72),
    "Ganges": ("Indian Ocean", 8, 0.63),
    "Rio Grande de Mindanao": ("North Pacific", 9, 0.54),
    "Agno": ("North Pacific", 10, 0.47),
    "Motagua": ("North Atlantic", None, None),
    "Mississippi": ("North Atlantic", None, None),
    "Amazon": ("South Atlantic", None, None),
    "Congo": ("South Atlantic", None, None),
    "Yangtze": ("North Pacific", None, None),
    "Yellow River": ("North Pacific", None, None),
    "Pearl River": ("North Pacific", None, None),
    "Mekong": ("North Pacific", None, None),
    "Tijuana": ("North Pacific", None, None),
    "Guayas": ("South Pacific", None, None),
    "Fly River": ("South Pacific", None, None),
    "Sepik": ("South Pacific", None, None),
    "Rhine": ("North Atlantic", None, None),
    "St. Lawrence": ("North Atlantic", None, None),
    "Niger": ("North Atlantic", None, None),
    "Orinoco": ("North Atlantic", None, None),
    "Indus": ("Indian Ocean", None, None),
    "Irrawaddy": ("Indian Ocean", None, None),
    "Citarum": ("Indian Ocean", None, None),
    "Mackenzie": ("Arctic Ocean", None, None),
    "Lena": ("Arctic Ocean", None, None),
    "Ob": ("Arctic Ocean", None, None),
    "Yenisei": ("Arctic Ocean", None, None),
}

COUNTRIES = {'Pasig': 'Philippines', 'Klang': 'Malaysia', 'Ulhas': 'India', 'Tullahan': 'Philippines', 'Meycauayan': 'Philippines', 'Pampanga': 'Philippines', 'Libmanan': 'Philippines', 'Ganges': 'India/Bangladesh', 'Rio Grande de Mindanao': 'Philippines', 'Agno': 'Philippines', 'Motagua': 'Guatemala/Honduras', 'Mississippi': 'United States', 'Amazon': 'Peru/Colombia/Brazil', 'Congo': 'DR Congo/Republic of the Congo', 'Yangtze': 'China', 'Yellow River': 'China', 'Pearl River': 'China', 'Mekong': 'China/Myanmar/Laos/Thailand/Cambodia/Vietnam', 'Tijuana': 'Mexico/United States', 'Guayas': 'Ecuador', 'Fly River': 'Papua New Guinea', 'Sepik': 'Papua New Guinea', 'Rhine': 'Switzerland/Germany/Netherlands', 'St. Lawrence': 'Canada/United States', 'Niger': 'Guinea/Mali/Niger/Nigeria', 'Orinoco': 'Venezuela/Colombia', 'Indus': 'China/India/Pakistan', 'Irrawaddy': 'Myanmar', 'Citarum': 'Indonesia', 'Mackenzie': 'Canada', 'Lena': 'Russia', 'Ob': 'Russia', 'Yenisei': 'Russia'}

# Single river selector, organized into two categories.
MAJOR_RIVERS = [
    "Amazon", "Mississippi", "Congo", "Yangtze",
    "Ganges", "Mekong", "Yellow River", "Pearl River",
    "Orinoco", "Niger", "Indus", "Irrawaddy",
    "Rhine", "St. Lawrence", "Mackenzie",
    "Lena", "Ob", "Yenisei"
]

POLLUTED_RIVERS = [
    name for name, data in RIVERS.items()
    if data[1] is not None
]

# Streamlit selectbox does not support native group headings,
# so group labels are included as non-selectable-looking separators.

# Selected 20 rivers for historical plastic simulations.
SELECTED_RIVERS = ['Pasig', 'Klang', 'Ulhas', 'Ganges', 'Mekong', 'Indus', 'Yangtze', 'Pearl River', 'Amazon', 'Mississippi', 'Motagua', 'Congo', 'Niger', 'Rhine', 'Yellow River', 'Orinoco', 'Citarum', 'Tijuana', 'Guayas', 'Fly River']

assert len(SELECTED_RIVERS) == 20
assert len(set(SELECTED_RIVERS)) == 20
assert all(name in RIVERS for name in SELECTED_RIVERS)

river_options = (
    ["── Major Rivers ──"]
    + [name for name in MAJOR_RIVERS if name in SELECTED_RIVERS]
    + ["── Plastic-Polluting Rivers ──"]
    + [name for name in SELECTED_RIVERS if name not in MAJOR_RIVERS]
)

location = st.selectbox(
    "River",
    river_options,
    index=None,
    placeholder="Select a river",
    format_func=lambda name: (
        f"{name} ({COUNTRIES[name]})"
        if name in COUNTRIES else name
    )
)

if location is not None and location.startswith("──"):
    location = None



# Historical trajectories for the smooth browser-side animation.
historical_lon = None
historical_lat = None

if location in HISTORICAL_RIVERS:
    dataset_path, output_hours = HISTORICAL_RIVERS[location]

    @st.cache_data(show_spinner="Loading historical river trajectories...")
    def load_historical_river(path):
        with xr.open_dataset(path) as ds:
            return ds["lon"].values.copy(), ds["lat"].values.copy()

    river_lon, river_lat = load_historical_river(dataset_path)

    selection_key = f"historical_particle_{location}"

    if selection_key not in st.session_state:
        st.session_state[selection_key] = 0

    selected_river_particle = st.sidebar.selectbox(
        "Particle trajectory",
        range(river_lon.shape[0]),
        key=selection_key,
        format_func=lambda i: f"Particle {i + 1}"
    )

    historical_lon = river_lon[selected_river_particle]
    historical_lat = river_lat[selected_river_particle]

st.markdown("### River Watershed Dashboard")

map_col, info_col = st.columns([4, 1], gap="small")

with map_col:
    if historical_lon is not None:
        render_top_model(historical_lon, historical_lat, output_hours)
    else:
        from top_model_renderer import load_land
        import plotly.graph_objects as go
        import streamlit.components.v1 as components

        land = load_land()
        fig_global = go.Figure()

        for feature in land["features"]:
            geometry = feature.get("geometry")
            if not geometry:
                continue

            if geometry["type"] == "Polygon":
                polygons = [geometry["coordinates"]]
            elif geometry["type"] == "MultiPolygon":
                polygons = geometry["coordinates"]
            else:
                continue

            for polygon in polygons:
                ring = polygon[0]
                segments = []
                current = []

                for point in ring:
                    x, y = point[:2]
                    if current and abs(x - current[-1][0]) > 180:
                        if len(current) >= 3:
                            segments.append(current)
                        current = []
                    current.append((x, y))

                if len(current) >= 3:
                    segments.append(current)

                for segment in segments:
                    fig_global.add_trace(go.Scatter(
                        x=[pt[0] for pt in segment],
                        y=[pt[1] for pt in segment],
                        mode="lines",
                        fill="toself",
                        fillcolor="#263746",
                        line=dict(color="#7890a0", width=0.6),
                        hoverinfo="skip",
                        showlegend=False
                    ))

        fig_global.update_layout(
            height=650,
            margin=dict(l=55, r=20, t=65, b=65),
            paper_bgcolor="#071c35",
            plot_bgcolor="#071c35",
            font=dict(color="white"),
            xaxis=dict(
                range=[-180, 180],
                title="Longitude",
                gridcolor="#31465c"
            ),
            yaxis=dict(
                range=[-90, 90],
                title="Latitude",
                gridcolor="#31465c",
                scaleanchor="x",
                scaleratio=1.22
            ),
            showlegend=False
        )

        components.html(
            fig_global.to_html(
                full_html=False,
                include_plotlyjs=True
            ),
            height=760,
            scrolling=False
        )

with info_col:
    st.markdown("#### Watershed characteristics")

    if location in RIVERS:
        st.markdown(f"**{location} River**")
        st.caption(f"Receiving ocean: {RIVERS[location][0]}")
    else:
        st.markdown("**North Pacific demonstration**")

    import csv

    environmental_data = {}
    csv_path = Path(__file__).resolve().parent.parent / "river_environment.csv"

    if csv_path.exists():
        with open(csv_path, newline="") as f:
            environmental_data = {
                row["river"]: row
                for row in csv.DictReader(f)
            }

    env = environmental_data.get(location, {})

    def metric_value(field, suffix="", decimals=1):
        raw = env.get(field, "")
        if not raw or not raw.strip():
            return "Data pending"
        try:
            value = float(raw)
            return f"{value:,.{decimals}f}{suffix}"
        except ValueError:
            return "Data pending"

    st.metric(
        "Watershed population",
        metric_value("watershed_population", decimals=0)
    )

    st.metric(
        "Mismanaged plastic waste",
        metric_value(
            "mismanaged_plastic_kg_person_year",
            " kg/person/year", 2
        )
    )
    st.caption(
        "Country-level · 2019 · Meijer et al. (2021) "
        "via Our World in Data"
    )

    st.metric(
        "Annual rainfall",
        metric_value("annual_rainfall_mm", " mm/year", 0)
    )
    st.caption("Watershed-average precipitation")

    if env.get("source", "").strip():
        st.caption(
            f"Source: {env['source']} "
            f"({env.get('reference_year', 'year unspecified')})"
        )

    st.divider()
    st.caption(
        "Environmental indicators will include source, "
        "reference year, and geographic coverage."
    )
