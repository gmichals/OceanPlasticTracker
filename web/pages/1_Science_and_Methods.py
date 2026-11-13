import streamlit as st

st.set_page_config(
    page_title="Science & Methods | Ocean Plastic Tracker",
    page_icon="🌊",
    layout="wide",
)

st.title("Science & Methods")
st.subheader("How does plastic move through the world's oceans?")

st.markdown("""
Rivers transport plastic waste from terrestrial environments into
coastal waters. Once plastic enters the ocean, its movement is
influenced by ocean currents, turbulent mixing, winds, and
interactions with coastlines.

The **Ocean Plastic Tracker** allows students to explore potential
transport pathways using numerical particle-tracking simulations.

## How the model works

The tracker uses a **Lagrangian particle-tracking approach**,
implemented with the OceanParcels framework.

Rather than observing ocean water at fixed locations, a Lagrangian
model follows individual particles as they move through a
time-varying velocity field.

The basic transport equation is:
""")

st.latex(r"\frac{d\mathbf{x}}{dt}=\mathbf{u}(\mathbf{x},t)")

st.markdown("""
Here, **x** represents particle position, **u** is the ocean
current velocity, and **t** is time.

## Physical processes

### Ocean circulation
Large-scale currents transport floating material along coastlines,
through boundary currents, and into the open ocean. Subtropical
gyres can retain floating material for extended periods.

### Turbulent dispersion
Small-scale ocean motions can cause particles released from the
same location to follow different trajectories.

### Coastline interactions
Floating material may become stranded along coastlines or return
to the ocean. Numerical models approximate these processes using
simplified rules.

## Explore 20 years of transport

The current tracker includes historical simulations for 20 river
systems, with 20 numerical particles per river and approximately
20 years of daily particle positions.

These simulations allow students to compare transport pathways
across ocean basins.

## Questions to investigate

1. How quickly do particles leave coastal waters?
2. Do particles from different rivers enter the same ocean gyres?
3. How do pathways differ among ocean basins?
4. Can particles move between ocean basins?
5. Why do particles from the same river follow different paths?

## Model limitations

The tracker illustrates potential transport pathways rather than
predicting the precise destination of individual plastic objects.

Numerical particles do not represent a specified mass of plastic.
The model does not fully resolve fragmentation, biological fouling,
sinking, or the diversity of real plastic materials.

The trajectories are historical simulations, not live observations
or forecasts of present-day plastic pollution.

**Key concept:** Ocean circulation connects distant coastlines,
river systems, and marine environments over years to decades.
""")

st.info(
    "Return to the Ocean Plastic Tracker using the navigation menu "
    "to explore the simulations."
)
