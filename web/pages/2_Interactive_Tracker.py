import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from top_model_renderer import render_top_model
from historical_river_datasets import HISTORICAL_RIVERS
import streamlit as st

if st.button("← Back to Home", key="back_to_home"):
    st.switch_page("web/Home.py")


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

    import random

    selection_key = f"random_particle_{location}"
    n_particles = river_lon.shape[0]

    if n_particles == 0:
        st.error("No particle trajectories available.")
        st.stop()

    if selection_key not in st.session_state:
        st.session_state[selection_key] = random.randrange(n_particles)

    selected_river_particle = st.session_state[selection_key]

    st.caption(
        f"Tracking particle #{selected_river_particle + 1} "
        f"of {n_particles} from the {location} River"
    )

    if st.button("🔀 Start Again — New Random Particle",
                 key=f"new_particle_{location}"):
        if n_particles > 1:
            choices = [
                i for i in range(n_particles)
                if i != selected_river_particle
            ]
            selected_river_particle = random.choice(choices)

        st.session_state[selection_key] = selected_river_particle
        st.rerun()

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
    if location in RIVERS:
        import csv
        import html

        environmental_data = {}
        csv_path = Path(__file__).resolve().parent.parent / "river_environment.csv"

        if csv_path.exists():
            with open(csv_path, newline="") as f:
                environmental_data = {
                    row["river"]: row
                    for row in csv.DictReader(f)
                }

        env = environmental_data.get(location, {})

        def metric_value(field, suffix="", decimals=1, compact=False):
            raw = env.get(field, "")
            if not raw or not raw.strip():
                return "Data pending"
            try:
                value = float(raw)
                if compact and abs(value) >= 1_000_000:
                    return f"{value / 1_000_000:,.1f} million"
                if compact and abs(value) >= 1_000:
                    return f"{value / 1_000:,.1f} thousand"
                return f"{value:,.{decimals}f}{suffix}"
            except ValueError:
                return "Data pending"

        if location in RIVERS:
            river_name = f"{location} River"
            ocean = RIVERS[location][0]
        else:
            river_name = "North Pacific"
            ocean = "Demonstration"

        population = metric_value(
            "watershed_population", decimals=0, compact=True
        )
        waste = metric_value(
            "mismanaged_plastic_kg_person_year",
            " kg/person/year", 2
        )
        rainfall = metric_value(
            "annual_rainfall_mm", " mm/year", 0
        )

        source = env.get("source", "").strip()
        reference_year = env.get("reference_year", "").strip()

        source_text = (
            f"Source: {source} ({reference_year or 'year unspecified'})"
            if source else "Source information pending"
        )

        def safe(value):
            return html.escape(str(value))

        st.markdown(f"""
        <style>
        .watershed-panel {{
            font-family: inherit;
            overflow-wrap: anywhere;
        }}
        .watershed-panel .river-title {{
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 0.3rem;
        }}
        .watershed-panel .ocean-label {{
            font-size: 0.82rem;
            color: #82909d;
            margin-bottom: 1.2rem;
        }}
        .watershed-panel .section-label {{
            font-size: 0.70rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            color: #82909d;
            margin-bottom: 0.8rem;
        }}
        .watershed-panel .metric-block {{
            padding: 0.7rem 0;
            border-bottom: 1px solid rgba(128,128,128,0.18);
        }}
        .watershed-panel .metric-label {{
            font-size: 0.80rem;
            color: inherit;
            opacity: 0.78;
            margin-bottom: 0.25rem;
        }}
        .watershed-panel .metric-number {{
            font-size: 1.22rem;
            font-weight: 600;
            line-height: 1.35;
            overflow-wrap: anywhere;
        }}
        .watershed-panel .metric-note {{
            font-size: 0.72rem;
            color: #82909d;
            line-height: 1.5;
            margin-top: 0.35rem;
        }}
        .watershed-panel .source-note {{
            font-size: 0.70rem;
            color: #82909d;
            line-height: 1.55;
            margin-top: 1rem;
        }}
        </style>

        <div class="watershed-panel">
          <div class="river-title">{safe(river_name)}</div>
          <div class="ocean-label">Receiving ocean: {safe(ocean)}</div>

          <div class="section-label">WATERSHED CHARACTERISTICS</div>

          <div class="metric-block">
            <div class="metric-label">Watershed population</div>
            <div class="metric-number">{safe(population)}</div>
          </div>

          <div class="metric-block">
            <div class="metric-label">Mismanaged plastic waste</div>
            <div class="metric-number">{safe(waste)}</div>
            <div class="metric-note">Country-level · 2019 · Meijer et al. (2021)</div>
          </div>

          <div class="metric-block">
            <div class="metric-label">Annual precipitation</div>
            <div class="metric-number">{safe(rainfall)}</div>
            <div class="metric-note">Watershed-average precipitation</div>
          </div>

          <div class="source-note">{safe(source_text)}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("### Understanding River Plastic Emissions")

        st.markdown("""
        **Watershed population**

        People living within the river's drainage basin.
        Used to estimate total plastic waste generation.

        **Mismanaged plastic waste (MPW)**

        Plastic waste inadequately collected or disposed of
        (kg/person/year). Combined with population, it
        estimates the waste potentially available for transport.

        **Annual precipitation**

        Average watershed rainfall (mm/year).
        Rainfall and runoff help move plastic from land
        into rivers and toward the ocean.

        **Watershed area**

        Land area draining into the river (km²).
        Helps characterize the drainage system and
        hydrological transport potential.

        **River plastic flux**

        Estimated plastic mass entering the ocean
        (tonnes/year). Only a fraction of mismanaged
        waste reaches the ocean because plastic may
        be retained on land or within rivers.

        ---

        *Based on the river plastic emission framework
        of Meijer et al. (2021), Science Advances.
        These variables help explain emissions but
        do not independently constitute a calibrated
        flux calculation.*
        """)
