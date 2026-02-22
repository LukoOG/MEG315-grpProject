def analyze_ad(m_biomass, vs_fraction, methane_yield):

    rho_ch4 = 0.716  # kg/m3
    LHV_CH4 = 50000  # kJ/kg

    m_vs = m_biomass * vs_fraction
    digestate_mass = m_biomass - m_vs

    volume_ch4 = methane_yield * m_vs
    m_ch4 = volume_ch4 * rho_ch4

    biogas_energy = m_ch4 * LHV_CH4  # kW

    return {
        "m_biomass": m_biomass,
        "m_vs": m_vs,
        "digestate_mass": digestate_mass,
        "m_ch4": m_ch4,
        "biogas_energy": biogas_energy
    }