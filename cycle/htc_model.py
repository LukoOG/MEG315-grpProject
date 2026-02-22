def analyze_htc(digestate_mass, char_yield, densification, htc_eff):
    """
    digestate_mass : kg/s
    char_yield     : mass fraction retained as hydrochar
    densification  : HHV improvement factor
    htc_eff        : energy retention efficiency
    """

    # Typical wet digestate heating value
    base_HHV = 15000  # kJ/kg (engineering assumption)

    # Mass of hydrochar produced
    m_char = digestate_mass * char_yield

    # Improved heating value
    char_HHV = base_HHV * densification

    # Energy rate of hydrochar (kW)
    hydrochar_energy = m_char * char_HHV * htc_eff

    return {
        "digestate_mass": digestate_mass,
        "hydrochar_mass": m_char,
        "char_HHV": char_HHV,
        "hydrochar_energy": hydrochar_energy
    }