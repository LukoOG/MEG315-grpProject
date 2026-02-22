import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def plot_ts(results):

    T = [results["T1"], results["T2"], results["T3"], results["T4"], results["T1"]]
    s = [1, 2, 3, 4, 1]

    fig, ax = plt.subplots(figsize=(4, 3))  # Smaller figure
    ax.plot(s, T, marker='o')
    ax.set_xlabel("Entropy (arb. units)", fontsize=8)
    ax.set_ylabel("Temperature (K)", fontsize=8)
    ax.set_title("Brayton T-s", fontsize=10)
    ax.tick_params(labelsize=7)

    fig.tight_layout()
    return fig


def plot_hs(results):

    h = [results["h1"], results["h2"], results["h3"], results["h4"], results["h1"]]
    s = [1, 2, 3, 4, 1]

    fig, ax = plt.subplots(figsize=(4, 3))  # Smaller figure
    ax.plot(s, h, marker='o')
    ax.set_xlabel("Entropy (arb. units)", fontsize=8)
    ax.set_ylabel("Enthalpy (J/kg)", fontsize=8)
    ax.set_title("Rankine h-s", fontsize=10)
    ax.tick_params(labelsize=7)

    fig.tight_layout()
    return fig