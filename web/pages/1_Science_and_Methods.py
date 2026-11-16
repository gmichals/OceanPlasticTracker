from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Science & Methods | Ocean Plastic Tracker",
    page_icon="🌊",
    layout="wide",
)

st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.science-hero {
    background: linear-gradient(120deg, #071b32, #075c76);
    padding: 48px 42px;
    border-radius: 16px;
    margin-bottom: 28px;
}
.science-hero h1 {
    color: #ffffff;
    font-size: 3rem;
    line-height: 1.15;
    margin-bottom: 12px;
}
.science-hero p {
    color: #d2eaf2;
    font-size: 1.15rem;
}
.eyebrow {
    color: #7ce1e9 !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px;
    font-weight: 700;
}
.section-number {
    color: #008eaa;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Refined scientific typography */
@media (min-width: 769px) {
    .stMarkdown h2 {
        font-size: 1.65rem !important;
        line-height: 1.3 !important;
        color: #087f9c !important;
        font-weight: 650 !important;
    }
}

.stMarkdown p, .stMarkdown li {
    font-size: 1.12rem;
    line-height: 1.75;
}

.section-number {
    color: #00a7bd !important;
    font-size: 0.82rem !important;
    font-weight: 750;
}

@media (max-width: 768px) {
    .stMarkdown h2 {
        font-size: 1.4rem !important;
        color: #087f9c !important;
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 1.05rem;
        line-height: 1.65;
    }
    .science-hero {
        padding: 25px 20px;
    }
    .science-hero h1 {
        font-size: 2rem;
    }
}


/* SCIENCE TYPOGRAPHY V2 */
[data-testid="stMain"] h2 {
    font-size: 1.55rem !important;
    color: #0095B3 !important;
    font-weight: 650 !important;
    line-height: 1.3 !important;
}

[data-testid="stMain"] [data-testid="stMarkdownContainer"] p {
    font-size: 19px !important;
    line-height: 1.8 !important;
}

[data-testid="stMain"] [data-testid="stMarkdownContainer"] li {
    font-size: 19px !important;
    line-height: 1.7 !important;
}

@media (max-width: 768px) {
    [data-testid="stMain"] h2 {
        font-size: 1.35rem !important;
    }
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMain"] [data-testid="stMarkdownContainer"] li {
        font-size: 17px !important;
    }
}

</style>
<div class="science-hero">
    <p class="eyebrow">THE SCIENCE BEHIND THE SIMULATION</p>
    <h1>How Does Plastic Travel Across an Ocean?</h1>
    <p>From river mouths to ocean gyres: understanding the physics
    of floating particle transport.</p>
</div>
""", unsafe_allow_html=True)

a, b, c = st.columns(3)
a.metric("River systems", "20")
b.metric("Simulation duration", "~20 years")
c.metric("Numerical particles", "400")

st.divider()


st.markdown(
    '<span class="section-number">01 / FROM RIVERS TO THE OCEAN</span>',
    unsafe_allow_html=True
)
# AMAZON RIVER PLUME FIGURE
st.divider()
st.header("From Rivers to the Open Ocean")

st.write("""
Rivers transport water, sediments, nutrients, and plastic debris
from continents into the coastal ocean.

Once released, floating plastic can be transported by coastal
currents, wind-driven circulation, and larger ocean currents.
Some particles remain near shore, while others may reach the
open ocean.

The Amazon River provides a striking example of how river-derived
material spreads into the Atlantic Ocean.
""")

st.image(
    str(Path(__file__).resolve().parent.parent /
        "assets/science/amazon_river_plume.jpg"),
    use_container_width=True,
)

st.caption(
    'Figure 1. Amazon River plume. NASA satellite imagery illustrating the transport of suspended sediment from the Amazon River into the Atlantic Ocean. The visible sediment plume is not a direct observation of plastic. Source: NASA Earth Observatory.'
)

st.write("""
**How this relates to our tracker:** The simulation releases
virtual particles near selected river mouths and follows their
subsequent movement through modeled ocean currents. These
trajectories represent possible transport pathways rather than
direct observations of plastic concentrations.
""")

st.divider()

st.markdown('<span class="section-number">02 / THE BIG PICTURE</span>',
            unsafe_allow_html=True)
st.header("The Ocean Is Always Moving")

# NASA CIRCULATION FIGURE
st.image(
    str(Path(__file__).resolve().parent.parent /
        "NASA circulation.png"),
    use_container_width=True,
)

st.caption(
    "Figure 2. Global ocean circulation. NASA's Perpetual Ocean visualization illustrates the complex structure of ocean currents and eddies. This is a NASA ocean-model visualization, not output from the Ocean Plastic Tracker. Source: NASA Scientific Visualization Studio."
)


st.write("""
The ocean is a dynamic system of currents, eddies, and large-scale
circulation patterns. Surface currents are influenced by winds,
Earth's rotation, pressure gradients, and the distribution of
temperature and salinity.

When floating material enters the ocean, it becomes part of this
moving system. Plastic released near one coastline can remain in
coastal waters, move into the open ocean, or travel across entire
ocean basins.

Subtropical ocean gyres are especially important because their
circulation can create regions where floating material accumulates.
However, an ocean gyre is not a stationary whirlpool, and not every
particle entering a gyre remains there.
""")

st.markdown('<span class="section-number">03 / THE NUMERICAL MODEL</span>',
            unsafe_allow_html=True)
st.header("Following Particles Through the Ocean")

st.write("""
The Ocean Plastic Tracker uses **OceanParcels**, a Lagrangian
particle-tracking framework.

In an Eulerian description, ocean velocity is measured at fixed
locations. In a Lagrangian description, we follow the position of
individual particles as they move through the velocity field.

The simplest mathematical description of particle motion is:
""")

st.latex(r"\frac{d\mathbf{x}}{dt}=\mathbf{u}(\mathbf{x},t)")

st.image(
    str(Path(__file__).resolve().parent.parent / "assets/science/lagrangian_advection.gif"),
    use_container_width=True,
)

st.caption(
    'Figure 3. Lagrangian particle advection. Original educational animation showing particles transported by an idealized ocean velocity field. This demonstrates the particle-tracking principle rather than actual historical ocean conditions.'
)


st.write("""
Here, **x** is particle position, **u** is the local ocean current
velocity, and **t** is time.

At each numerical time step, the model estimates the ocean velocity
at the particle's position and updates its location. Repeating
this calculation generates a trajectory.

The ocean currents are provided by historical ocean circulation
data rather than calculated directly by the particle tracker.
""")

st.markdown('<span class="section-number">04 / TURBULENT DISPERSION</span>',
            unsafe_allow_html=True)
st.header("Why Do Particles Follow Different Paths?")

st.write("""
Ocean currents contain motions across a wide range of spatial and
temporal scales. Even high-resolution circulation products cannot
resolve every small eddy and turbulent fluctuation.

Particle-tracking models can approximate unresolved horizontal
mixing by adding stochastic displacements to the motion caused by
resolved ocean currents.

A simplified stochastic transport equation is:
""")

st.latex(
    r"d\mathbf{x}=\mathbf{u}(\mathbf{x},t)\,dt"
    r"+\sqrt{2K_h}\,d\mathbf{W}"
)

st.image(
    str(Path(__file__).resolve().parent.parent /
        "assets/science/turbulent_diffusion.gif"),
    use_container_width=True,
)

st.caption(
    'Figure 4. Turbulent particle dispersion. Original educational animation showing how stochastic motion causes initially nearby particles to follow different paths while being transported by a common current. This is an idealized demonstration.'
)


st.write("""
Here, **Kₕ** represents horizontal diffusivity and **W** represents
a random process.

This formulation illustrates why particles released near the same
location can gradually separate. The degree of separation depends
on ocean circulation and the diffusion parameterization.

The precise diffusion settings used in our historical simulations
will be documented separately.
""")


st.markdown(
    '<span class="section-number">05 / OCEAN GYRES</span>',
    unsafe_allow_html=True
)
st.header("Why Does Plastic Accumulate in Ocean Gyres?")

st.write("""
The major subtropical ocean gyres are large circulation systems
formed by wind-driven currents, Earth's rotation, and the geometry
of the ocean basins.

Floating debris can accumulate in regions where surface transport
converges. This convergence is influenced by wind-driven Ekman
transport and the surrounding ocean circulation.

**Circulation alone does not guarantee accumulation.**
A purely rotating current can move particles around a gyre without
bringing them closer together.

The animation below illustrates how rotation combined with weak
convergence can concentrate floating particles.
""")

st.image(
    str(Path(__file__).resolve().parent.parent /
        "assets/science/gyre_accumulation.gif"),
    use_container_width=True,
)

st.caption(
    'Figure 5. Gyre circulation and convergence. Original educational animation illustrating how rotation combined with weak inward transport can produce particle accumulation. Rotation alone does not guarantee accumulation. This is not a quantitative garbage-patch prediction.'
)

st.info(
    "A garbage patch is not a solid island of plastic. "
    "It is a broad region where floating debris may be more "
    "concentrated than in surrounding waters."
)

st.markdown('<span class="section-number">06 / COASTAL PROCESSES</span>',
            unsafe_allow_html=True)
st.header("What Happens When Plastic Reaches Land?")

st.write("""
Coastal transport is particularly challenging to simulate.

Real plastic debris may become stranded on beaches, remain trapped
in estuaries, or return to the ocean through waves, tides, and
storms.

Our particle-tracking workflow includes simplified coastline
interactions, including numerical approaches to coastline avoidance
and beaching/refloating.

These approximations are useful for exploring potential transport
pathways, but they do not reproduce every physical process occurring
along a real shoreline.
""")

st.markdown('<span class="section-number">07 / INTERPRETING RESULTS</span>',
            unsafe_allow_html=True)
st.header("What Can the Simulations Tell Us?")

st.write("""
The current Ocean Plastic Tracker contains historical simulations
for 20 river systems, with 20 numerical particles released for each
river.

The resulting trajectories illustrate possible pathways of
floating material through the global ocean circulation system.

They allow comparisons between river sources, ocean basins, and
individual particle histories.

However, the numerical particles do not represent a specified
mass of plastic. The simulations should not be interpreted as
predictions of plastic concentration, total pollution mass, or
the probability of debris reaching a particular destination.
""")

st.info(
    "Scientific distinction: A particle trajectory describes a "
    "possible transport pathway. Estimating plastic accumulation "
    "requires additional assumptions about emissions, particle "
    "properties, loss processes, and statistical sampling."
)

st.markdown('<span class="section-number">08 / EXPLORE</span>',
            unsafe_allow_html=True)
st.header("Investigate the Global Ocean")

st.write("""
Use the interactive tracker to compare river systems and investigate
how ocean circulation connects distant marine environments.

Try following particles from the Amazon, Mississippi, Yangtze,
Ganges, and Congo rivers. Compare their pathways and consider
how ocean basin geometry influences transport.
""")

if st.button("🌍 Launch Interactive Tracker", type="primary"):
    st.switch_page("pages/2_Interactive_Tracker.py")

st.divider()
st.caption(
    "Ocean Plastic Tracker | Educational particle-transport simulations "
    "using OceanParcels and historical ocean circulation data."
)


# MPW_TO_OCEAN_METHODS_SECTION
st.markdown(r"""
## From plastic waste generation to ocean plastic flux

### 1. Plastic waste generation

Annual plastic waste generation is estimated using population
and plastic waste generated per person:

$$
W_i = N_i \times w_i
$$

where $N_i$ is population and $w_i$ is annual plastic waste
generation per person in geographic grid cell $i$.

### 2. Mismanaged plastic waste (MPW)

Mismanaged plastic waste is the portion of generated waste
that is inadequately collected or disposed of.

$$
MPW_i = W_i \times f_{\mathrm{mismanaged},i}
$$

The mismanaged fraction reflects waste-management conditions,
including collection coverage and disposal practices.

MPW represents potential environmental plastic pollution.
It does not mean that all this plastic enters a river or ocean.

### 3. Calculating river-to-ocean plastic flux

In the conceptual framework of Meijer et al. (2021),
the annual ocean plastic flux is calculated by combining
spatially distributed MPW with modeled transport probabilities:

$$
F_{\mathrm{ocean}} =
\sum_{i=1}^{n}
MPW_i \, P(M)_i \, P(R)_i \, P(O)_i
$$

**Definitions:**

- **Σ (capital Greek letter sigma)** means **sum**:
  add together the contributions from all geographic grid cells.
- **i** identifies an individual grid cell.
- **n** is the total number of grid cells in the watershed.
- **MPW** is annual mismanaged plastic waste.
- **P(M)** is the probability of plastic mobilization,
  influenced by rainfall and wind.
- **P(R)** is the probability of reaching a river,
  influenced by distance, terrain, and land characteristics.
- **P(O)** is the probability of reaching the ocean,
  influenced by river transport and retention.

The probabilities vary geographically. Consequently,
two watersheds producing similar amounts of mismanaged
plastic waste may deliver very different amounts to the ocean.

### 4. How Ocean Plastic Tracker uses these estimates

Our tracker separates two processes:

1. **River-to-ocean emissions:** Published modeled estimates
   provide the amount of plastic entering the ocean from rivers.
2. **Ocean transport:** OceanParcels simulates the subsequent
   movement of plastic particles using ocean-current forcing
   and the transport processes implemented in the tracker.

The tracker does not currently reproduce the complete
Meijer land-to-ocean emissions model.

Waste-generation indicators from Cottom et al. (2024)
provide additional watershed context. They should not
be confused with the original Meijer model inputs.

### 5. Uncertainty and limitations

River emissions are modeled estimates, not continuous
direct measurements. Uncertainty arises from population,
waste inventories, management practices, rainfall,
mobilization, transport, and model calibration.

**Reference:** Meijer et al. (2021),
*Science Advances*, 7, eaaz5803.

https://doi.org/10.1126/sciadv.aaz5803
""")
