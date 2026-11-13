from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Ocean Plastic Tracker",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.image(
    str(Path(__file__).parent / "NASA circulation.png"),
    use_container_width=True,
)

st.markdown("""
<h1 style="text-align:center;">Ocean Plastic Tracker</h1>
<p style="text-align:center; font-size:1.2rem;">
Follow the journey of river-borne plastic through the world's oceans.
</p>
<p style="text-align:center;">
20 Rivers · 20 Years · Global Ocean Circulation
</p>
""", unsafe_allow_html=True)

st.caption(
    "Ocean circulation visualization: NASA Scientific Visualization Studio."
)

st.write("")
st.write("")

left, right = st.columns(2, gap="large")

with left:
    st.subheader("🔬 Explore the Science")
    st.write(
        "Discover how ocean currents, turbulent dispersion, and "
        "coastline interactions influence the movement of plastic."
    )
    if st.button("Science & Methods", use_container_width=True):
        st.switch_page("pages/1_Science_and_Methods.py")

with right:
    st.subheader("🌍 Launch the Tracker")
    st.write(
        "Choose a river and follow simulated particles across "
        "the world's oceans over approximately 20 years."
    )
    if st.button("Interactive Tracker", use_container_width=True):
        st.switch_page("pages/2_Interactive_Tracker.py")

st.divider()
st.caption(
    "An educational visualization of historical ocean transport "
    "using numerical particle-tracking simulations."
)
