from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent

pages = [
    st.Page(str(ROOT / "Home.py"), title="Home", icon="🏠", default=True),
    st.Page(str(ROOT / "supabase_connection_test.py"),
            title="Connection Test", icon="🔧"),
    st.Page(str(ROOT / "pages/1_Science_and_Methods.py"),
            title="Science & Methods", icon="🔬"),
    st.Page(str(ROOT / "pages/2_Interactive_Tracker.py"),
            title="Interactive Tracker", icon="🌊"),
]

navigation = st.navigation(pages)
navigation.run()
