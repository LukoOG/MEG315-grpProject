from CoolProp.CoolProp import PropsSI

def rankine_cycle(P_boiler, T_superheat, P_cond, eta_t, eta_p, m_steam):

    # Unit conversions
    # P_boiler = P_boiler * 1e6      # MPa → Pa (if input is MPa)
    # P_cond = P_cond * 1e3          # kPa → Pa (if input is kPa)
    # T_superheat = T_superheat + 273  # °C → K

    # State 1: saturated liquid at condenser pressure
    h1 = PropsSI("H","P",P_cond,"Q",0,"Water")
    s1 = PropsSI("S","P",P_cond,"Q",0,"Water")

    # Pump (isentropic + efficiency)
    h2s = PropsSI("H","P",P_boiler,"S",s1,"Water")
    h2 = h1 + (h2s - h1) / eta_p
    s2 = PropsSI("S","P",P_boiler,"H",h2,"Water")

    # Boiler + superheat
    h3 = PropsSI("H","P",P_boiler,"T",T_superheat,"Water")
    s3 = PropsSI("S","P",P_boiler,"T",T_superheat,"Water")

    # Turbine expansion
    h4s = PropsSI("H","P",P_cond,"S",s3,"Water")
    h4 = h3 - eta_t * (h3 - h4s)
    s4 = PropsSI("S","P",P_cond,"H",h4,"Water")

    # Work calculations
    Wt = m_steam * (h3 - h4)
    Wp = m_steam * (h2 - h1)

    eta_cycle = (Wt - Wp) / (m_steam * (h3 - h2))

    return {
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "h4": h4,
        "s1": s1,
        "s2": s2,
        "s3": s3,
        "s4": s4,
        "Turbine Work (kW)": Wt/1000,
        "Pump Work (kW)": Wp/1000,
        "Rankine Efficiency": eta_cycle,
        "Mass Flow Steam (kg/s)": m_steam
    }