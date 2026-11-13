import json
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
LAND = ROOT / "data/maps/ne_110m_land.geojson"

@st.cache_data
def load_land():
    return json.loads(LAND.read_text())


def render_global_map():
    """Show the TOP MODEL map at global extent before river selection."""
    land = load_land()
    fig = go.Figure()

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
                fig.add_trace(go.Scatter(
                    x=[p[0] for p in segment],
                    y=[p[1] for p in segment],
                    mode="lines",
                    fill="toself",
                    fillcolor="#263746",
                    line=dict(color="#7890a0", width=0.6),
                    hoverinfo="skip",
                    showlegend=False
                ))

    fig.update_layout(
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
        fig.to_html(full_html=False, include_plotlyjs=True),
        height=760,
        scrolling=False
    )


def render_top_model(lon_values, lat_values, output_hours=24):
    land = load_land()
    lon = np.asarray(lon_values, dtype=float)
    lat = np.asarray(lat_values, dtype=float)

    # Keep longitude continuous across the international date line.
    valid = np.isfinite(lon) & np.isfinite(lat)
    lon = np.rad2deg(np.unwrap(np.deg2rad(lon)))
    lon[~valid] = np.nan
    lat[~valid] = np.nan

    frame_step = max(1, round(30 * 24 / output_hours))
    indices = list(range(0, len(lon), frame_step))
    if indices[-1] != len(lon) - 1:
        indices.append(len(lon) - 1)

    def bounds(i):
        x = lon[:i + 1]
        y = lat[:i + 1]
        ok = np.isfinite(x) & np.isfinite(y)
        x, y = x[ok], y[ok]
        if len(x) == 0:
            return [110, 135], [20, 45]

        xmin, xmax = float(x.min()), float(x.max())
        ymin, ymax = float(y.min()), float(y.max())
        dx = max(xmax - xmin, 12)
        dy = max(ymax - ymin, 8)
        cx = (xmin + xmax) / 2
        cy = (ymin + ymax) / 2

        return [cx - dx * 0.85, cx + dx * 0.85], [cy - dy * 0.85, cy + dy * 0.85]

    # Precompute bounds for every displayed frame.
    frame_bounds = [bounds(i) for i in indices]

    fig = go.Figure()

    # Natural Earth background. Longitude copies support dateline crossings.
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

            # Split large longitude jumps to avoid diagonal lines across oceans.
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
                for shift in range(-720, 1081, 360):
                    fig.add_trace(go.Scatter(
                        x=[p[0] + shift for p in segment],
                        y=[p[1] for p in segment],
                        mode="lines",
                        fill="toself",
                        fillcolor="#263746",
                        line=dict(color="#7890a0", width=0.6),
                        hoverinfo="skip",
                        showlegend=False
                    ))

    # Track and particle are always the final two traces.
    track_index = len(fig.data)

    fig.add_trace(go.Scatter(
        x=[float(lon[0])],
        y=[float(lat[0])],
        mode="lines",
        line=dict(color="cyan", width=3),
        name="Particle trajectory"
    ))

    particle_index = len(fig.data)

    fig.add_trace(go.Scatter(
        x=[float(lon[0])],
        y=[float(lat[0])],
        mode="markers",
        marker=dict(color="yellow", size=12),
        name="Particle position"
    ))

    xrng, yrng = frame_bounds[0]

    fig.update_layout(
        height=650,
        margin=dict(l=55, r=20, t=65, b=65),
        paper_bgcolor="#071c35",
        plot_bgcolor="#071c35",
        font=dict(color="white"),
        xaxis=dict(range=xrng, title="Longitude", gridcolor="#31465c"),
        yaxis=dict(
            range=yrng,
            title="Latitude",
            gridcolor="#31465c",
            scaleanchor="x",
            scaleratio=1.22,
        ),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08),
    )

    # Create an HTML page with Plotly embedded and browser-side controls.
    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        div_id="trajectory_map",
        config={"responsive": True}
    )

    payload = json.dumps({
        "lon": [None if not np.isfinite(v) else float(v) for v in lon],
        "lat": [None if not np.isfinite(v) else float(v) for v in lat],
        "indices": indices,
        "output_hours": output_hours,
        "bounds": frame_bounds,
        "track_index": track_index,
        "particle_index": particle_index,
    })

    html = f"""
    <style>
    body {{
        margin: 0;
        background: #071c35;
        color: white;
        font-family: sans-serif;
    }}
    .controls {{
        display: flex;
        gap: 14px;
        align-items: center;
        padding: 10px 20px;
    }}
    button {{
        padding: 8px 16px;
        cursor: pointer;
    }}
    input[type=range] {{
        flex: 1;
    }}
    </style>

    {plot_html}

    <div class="controls">
        <button id="play">▶ Play</button>
        <button id="pause">⏸ Pause</button>
        <input id="slider" type="range" min="0" max="{len(indices)-1}" value="0">
        <span id="year">Year 0.0</span>
    </div>

    <script>
    const data = {payload};
    const graph = document.getElementById("trajectory_map");
    const slider = document.getElementById("slider");
    const year = document.getElementById("year");

    let frame = 0;
    let timer = null;

    function updateFrame(k) {{
        frame = k;
        const i = data.indices[k];

        Plotly.restyle(
            graph,
            {{
                x: [data.lon.slice(0, i + 1), [data.lon[i]]],
                y: [data.lat.slice(0, i + 1), [data.lat[i]]]
            }},
            [data.track_index, data.particle_index]
        );

        const b = data.bounds[k];

        Plotly.relayout(graph, {{
            "xaxis.range": b[0],
            "yaxis.range": b[1]
        }});

        slider.value = k;
        year.textContent = "Year " + (i * data.output_hours / (24 * 365)).toFixed(1);
    }}

    document.getElementById("play").onclick = () => {{
        if (timer !== null) return;

        timer = setInterval(() => {{
            if (frame >= data.indices.length - 1) {{
                clearInterval(timer);
                timer = null;
                return;
            }}
            updateFrame(frame + 1);
        }}, 120);
    }};

    document.getElementById("pause").onclick = () => {{
        clearInterval(timer);
        timer = null;
    }};

    slider.oninput = () => {{
        clearInterval(timer);
        timer = null;
        updateFrame(Number(slider.value));
    }};
    </script>
    """

    components.html(html, height=760, scrolling=False)
