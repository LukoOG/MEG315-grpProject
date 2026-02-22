import matplotlib.pyplot as plt

def plot_ts(results):

    T = [results["T1"], results["T2"], results["T3"], results["T4"], results["T1"]]
    s = [1,2,3,4,1]

    fig, ax = plt.subplots()
    ax.plot(s, T, marker='o')
    ax.set_xlabel("Entropy (s)")
    ax.set_ylabel("Temperature (K)")
    ax.set_title("Brayton T-s Diagram")

    return fig


def plot_hs(results):

    h = [results["h1"], results["h2"], results["h3"], results["h4"], results["h1"]]
    s = [1,2,3,4,1]

    fig, ax = plt.subplots()
    ax.plot(s, h, marker='o')
    ax.set_xlabel("Entropy (s)")
    ax.set_ylabel("Enthalpy (J/kg)")
    ax.set_title("Rankine h-s Diagram")

    return fig