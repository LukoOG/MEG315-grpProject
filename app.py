import streamlit as st
from cycle.ad_model import analyze_ad
from cycle.htc_model import analyze_htc
from cycle.gas_cycle import brayton_cycle
from cycle.steam_cycle import rankine_cycle
from plots.diagrams import plot_ts, plot_hs

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-font">Combined Cycle Power Plant Results</p>', unsafe_allow_html=True)

st.set_page_config(layout="wide")
st.title("AD-HTC Fuel Enhanced Combined Cycle Simulator")

st.sidebar.header("AD Parameters")

m_biomass = st.sidebar.number_input("Biomass flow (kg/s)", value=5.0)
vs_fraction = st.sidebar.slider("Volatile Solids Fraction", 0.1, 1.0, 0.8)
methane_yield = st.sidebar.number_input("Methane yield (m3/kg VS)", value=0.35)

st.sidebar.header("HTC Parameters")

char_yield = st.sidebar.slider("Hydrochar Yield Fraction", 0.3, 0.8, 0.6)
htc_eff = st.sidebar.slider("HTC Energy Efficiency", 0.5, 1.0, 0.85)
energy_density = st.sidebar.slider("Energy Density Factor", 1.0, 2.0, 1.5)

st.sidebar.header("Brayton Parameters")

T1 = st.sidebar.number_input("Compressor Inlet Temp (K)", value=300.0)
P1 = st.sidebar.number_input("Compressor Inlet Pressure (kPa)", value=100.0)
rp = st.sidebar.number_input("Pressure Ratio", value=8.0)
T3 = st.sidebar.number_input("Turbine Inlet Temp (K)", value=1200.0)
eta_c = st.sidebar.slider("Compressor Efficiency", 0.6, 1.0, 0.85)
eta_t_gas = st.sidebar.slider("Gas Turbine Efficiency", 0.6, 1.0, 0.9)
m_air = st.sidebar.number_input("Air Mass Flow (kg/s)", value=10.0)

st.sidebar.header("Rankine Parameters")

P_boiler = st.sidebar.number_input("Boiler Pressure (Pa)", value=8e6)
T_superheat = st.sidebar.number_input("Superheat Temp (K)", value=773.0)
P_cond = st.sidebar.number_input("Condenser Pressure (Pa)", value=10000.0)
eta_t_steam = st.sidebar.slider("Steam Turbine Efficiency", 0.6, 1.0, 0.9)
eta_p = st.sidebar.slider("Pump Efficiency", 0.6, 1.0, 0.85)
m_steam = st.sidebar.number_input("Steam Mass Flow (kg/s)", value=5.0)

# =========================
# RUN ANALYSIS
# =========================
if st.button("Run Integrated Analysis"):

    # --- AD ---
    ad = analyze_ad(m_biomass, vs_fraction, methane_yield)

    # --- HTC ---
    htc = analyze_htc(
        ad["digestate_mass"],
        char_yield,
        energy_density,
        htc_eff
    )

    # --- Fuel Energy ---
    fuel_energy = (
        ad["biogas_energy"] +
        htc["hydrochar_energy"]
    )

    # --- Brayton ---
    brayton_results = brayton_cycle(
        T1, P1, rp, T3,
        eta_c, eta_t_gas,
        m_air
    )

    # --- Rankine ---
    rankine_results = rankine_cycle(
        P_boiler, T_superheat, P_cond,
        eta_t_steam, eta_p,
        m_steam
    )

    # --- Power Calculation ---
    brayton_power = brayton_results["Net Work (kW)"]

    rankine_power = (
        rankine_results["Turbine Work (kW)"] -
        rankine_results["Pump Work (kW)"]
    )

    total_power = brayton_power + rankine_power

    overall_eff = total_power / fuel_energy

    st.subheader("System Efficiencies")
    # st.write("Brayton Efficiency:", brayton_results["Brayton Efficiency"])
    # st.write("Rankine Efficiency:", rankine_results["Rankine Efficiency"])
    # st.write("Overall System Efficiency:", overall_eff)
    
    brayton_eff = brayton_results["Brayton Efficiency"] * 100
    rankine_eff = rankine_results["Rankine Efficiency"] * 100

    st.metric("Brayton Efficiency (%)", f"{brayton_eff:.2f} %")
    st.metric("Rankine Efficiency (%)", f"{rankine_eff:.2f} %")
    st.metric("Overall System Efficiency (%)", f"{overall_eff:.2f} %")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Brayton Cycle")
        st.metric("Efficiency", f"{brayton_eff:.2f} %")
        st.metric("Mass Flow Air", f"{brayton_results['Mass Flow Air (kg/s)']:.2f} kg/s")
        st.metric("Net Work", f"{brayton_results['Net Work (kW)']:.2f} kW")

    with col2:
        st.subheader("Rankine Cycle")
        st.metric("Efficiency", f"{rankine_eff:.2f} %")
        st.metric("Mass Flow Steam", f"{rankine_results['Mass Flow Steam (kg/s)']:.2f} kg/s")
        st.metric("Net Work", f"{rankine_results['Rankine Net Work (kW)']:.2f} kW")

    with col3:
        st.subheader("Overall System")
        st.metric("Overall Efficiency", f"{overall_eff:.2f} %")
        st.metric("Total Power Output", f"{total_power:.2f} kW")

    st.pyplot(plot_ts(brayton_results))
    st.pyplot(plot_hs(rankine_results))