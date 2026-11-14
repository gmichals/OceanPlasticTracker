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
navigation.run()
