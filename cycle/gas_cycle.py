import numpy as np

def brayton_cycle(T1, P1, rp, T3, eta_c, eta_t, m_air):
    gamma = 1.4
    cp = 1005  # J/kg-K

    T2s = T1 * rp**((gamma-1)/gamma)
    T2 = T1 + (T2s - T1) / eta_c

    T4s = T3 * rp**(-(gamma-1)/gamma)
    T4 = T3 - eta_t * (T3 - T4s)

    Wc = m_air * cp * (T2 - T1)
    Wt = m_air * cp * (T3 - T4)
    Wnet = Wt - Wc

    Qin = m_air * cp * (T3 - T2)

    eta_cycle = Wnet / Qin

    Qin = cp * (T3 - T2)
    efficiency = Wnet / Qin

    exhaust_heat = cp * (T4 - T1)

    return {
        "T1": T1,
        "T2": T2,
        "T3": T3,
        "T4": T4,
        "Compressor Work (kW)": Wc,
        "Turbine Work (kW)": Wt,
        "Net Work (kW)": Wnet,
        "Heat Input (kW)": Qin,
        "Brayton Efficiency": eta_cycle,
        "Mass Flow Air (kg/s)": m_air,
        "Exhaust Temp (K)": T4
    }