from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent

pages = [
    st.Page(str(ROOT / "Home.py"), title="Home", icon="🏠", default=True),
    st.Page(str(ROOT / "pages/1_Science_and_Methods.py"),
            title="Science & Methods", icon="🔬"),
    st.Page(str(ROOT / "pages/2_Interactive_Tracker.py"),
            title="Interactive Tracker", icon="🌊"),
]


pages.append(
    st.Page(
        str(ROOT / "pages/3_Usage_Statistics.py"),
        title="Usage Statistics",
        icon="📊",
    )
)

navigation = st.navigation(pages)



import streamlit.components.v1 as components

# Track one visit per page per Streamlit session.
page_path = "/" + navigation.url_path if navigation.url_path else "/"

if "goatcounter_pages_seen" not in st.session_state:
    st.session_state["goatcounter_pages_seen"] = set()

if page_path not in st.session_state["goatcounter_pages_seen"]:
    st.session_state["goatcounter_pages_seen"].add(page_path)

    components.html(
        f"""
        <script>
        const params = new URLSearchParams({{
            p: {page_path!r},
            t: "Ocean Plastic Tracker"
        }});

        fetch(
            "https://oceanplastictracker.goatcounter.com/count?"
            + params.toString(),
            {{mode: "no-cors"}}
        );
        </script>
        """,
        height=0,
    )

navigation.run()
