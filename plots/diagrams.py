import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def plot_ts(results):

    T = [results["T1"], results["T2"], results["T3"], results["T4"], results["T1"]]
    s = [results["s1"], results["s2"], results["s3"], results["s4"], results["s1"]]

    fig, ax = plt.subplots(figsize=(5,4))

    ax.plot(s, T, marker='o')

    # Label each state
    for i, label in enumerate(["1","2","3","4"]):
        ax.text(s[i], T[i], f"  {label}", fontsize=10)

    ax.set_xlabel("Entropy (J/kg·K)", fontsize=11)
    ax.set_ylabel("Temperature (K)", fontsize=11)
    ax.set_title("Brayton Cycle T–s Diagram", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(s[1],T[1]), xytext=(s[0],T[0]),
            arrowprops=dict(arrowstyle="->"))

    ax.grid(True, linestyle="--", alpha=0.6)

    return fig


def plot_hs(results):

    h = [results["h1"], results["h2"], results["h3"], results["h4"], results["h1"]]
    s = [results["s1"], results["s2"], results["s3"], results["s4"], results["s1"]]

    fig, ax = plt.subplots(figsize=(5,4))

    ax.plot(s, h, marker='o')

    for i, label in enumerate(["1","2","3","4"]):
        ax.text(s[i], h[i], f"  {label}", fontsize=10)

    ax.set_xlabel("Entropy (J/kg·K)", fontsize=11)
    ax.set_ylabel("Enthalpy (J/kg)", fontsize=11)
    ax.set_title("Rankine Cycle h–s Diagram", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(s[1],h[1]), xytext=(s[0],h[0]),
            arrowprops=dict(arrowstyle="->"))

    ax.grid(True, linestyle="--", alpha=0.6)

    return fig