import numpy as np

def brayton_cycle(T1, P1, rp, T3, eta_c, eta_t, m_air):

    gamma = 1.4
    cp = 1005        # J/kg-K
    R = 287          # J/kg-K

    # ---- Pressures ----
    P2 = P1 * rp
    P3 = P2
    P4 = P1

    # ---- Compressor ----
    T2s = T1 * rp**((gamma-1)/gamma)
    T2 = T1 + (T2s - T1) / eta_c

    # ---- Turbine ----
    T4s = T3 * rp**(-(gamma-1)/gamma)
    T4 = T3 - eta_t * (T3 - T4s)

    # ---- Entropy (ideal gas relation) ----
    s1 = 0
    s2 = s1 + cp*np.log(T2/T1) - R*np.log(P2/P1)
    s3 = s2 + cp*np.log(T3/T2)
    s4 = s3 + cp*np.log(T4/T3) - R*np.log(P4/P3)

    # ---- Work (kW) ----
    Wc = m_air * cp * (T2 - T1) / 1000
    Wt = m_air * cp * (T3 - T4) / 1000
    Wnet = Wt - Wc

    # ---- Heat input (kW) ----
    Qin = m_air * cp * (T3 - T2) / 1000

    # ---- Efficiency ----
    eta_cycle = Wnet / Qin

    # ---- Exhaust heat available (kW) ----
    exhaust_heat = m_air * cp * (T4 - T1) / 1000

    return {
        "T1": T1,
        "T2": T2,
        "T3": T3,
        "T4": T4,
        "s1": s1,
        "s2": s2,
        "s3": s3,
        "s4": s4,
        "Compressor Work (kW)": Wc,
        "Turbine Work (kW)": Wt,
        "Net Work (kW)": Wnet,
        "Heat Input (kW)": Qin,
        "Brayton Efficiency": eta_cycle,
        "Mass Flow Air (kg/s)": m_air,
        "Exhaust Heat Available (kW)": exhaust_heat,
        "Exhaust Temp (K)": T4
    }