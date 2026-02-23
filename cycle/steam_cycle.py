from CoolProp.CoolProp import PropsSI

def rankine_cycle(P_boiler, T_superheat, P_cond, eta_t, eta_p, Q_available):

    # --- State 1 ---
    h1 = PropsSI("H","P",P_cond,"Q",0,"Water")
    s1 = PropsSI("S","P",P_cond,"Q",0,"Water")

    # --- Pump ---
    h2s = PropsSI("H","P",P_boiler,"S",s1,"Water")
    h2 = h1 + (h2s - h1) / eta_p
    s2 = PropsSI("S","P",P_boiler,"H",h2,"Water")

    # --- Boiler ---
    h3 = PropsSI("H","P",P_boiler,"T",T_superheat,"Water")
    s3 = PropsSI("S","P",P_boiler,"T",T_superheat,"Water")

    # 🔥 Heat required per kg steam
    q_boiler = h3 - h2   # J/kg

    # Convert Q_available from kW to W
    Q_available_W = Q_available * 1000

    # 🔗 Compute allowable steam mass flow
    m_steam = Q_available_W / q_boiler

    # --- Turbine ---
    h4s = PropsSI("H","P",P_cond,"S",s3,"Water")
    h4 = h3 - eta_t * (h3 - h4s)
    s4 = PropsSI("S","P",P_cond,"H",h4,"Water")

    # --- Work ---
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
        "Mass Flow Steam (kg/s)": m_steam,
        "Heat Input Used (kW)": Q_available
    }