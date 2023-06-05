# %%
import pandas as pd
import matplotlib.pyplot as plt

# Messdaten einlesen
df = pd.read_csv("data.csv")

# In der Tabelle sind die Kreislagen 1 und 2 als eigene Zeilen jeweils
# im Wechsel angeordnet. Zuerst müssen diese Messungen in eine Zeile
# zusammengefasst werden.
K1 = df[::2].reset_index(drop=True)
K2 = df[1::2].reset_index(drop=True)

df = pd.DataFrame(
    {
        "index": range(0, 24),
        "Messer": K1["Messer"],
        "Zielpunkt": K1["Zielpunkt"],
        "R1": K1["R"],
        "R2": K2["R"],
        "zeta1": K1["zeta"],
        "zeta2": K2["zeta"],
    }
)


# Berechnet den Komplementärwinkel zu einem Winkel x in gon.
def pm200(x):
    if x > 200:
        return x - 200
    else:
        return x + 200


# Indexfehler, Ziellinienfehler und Mittelwerte berechnen
df["c"] = 1 / 2 * (df["R2"].apply(pm200) - df["R1"])
df["R"] = 1 / 2 * (df["R1"] + df["R1"].apply(pm200))
df["i"] = 1 / 2 * (400 - (df["zeta1"] + df["zeta2"]))
df["zeta"] = 1 / 2 * (400 + (df["zeta1"] - df["zeta2"]))


# c und i in mgon umrechnen
df["c"] = 1000 * df["c"]
df["i"] = 1000 * df["i"]

# Ergebnisse speichern
df.to_csv("results.csv", index=False)

# Mittelwerte und Standardabweichungen berechnen
c_mean = df["c"].mean()
c_std = df["c"].std(ddof=1)
i_mean = df["i"].mean()
i_std = df["i"].std(ddof=1)

print(f"Ziellinienfehler c: {c_mean:.3f} ± {c_std:.3f} mgon")
print(f"Indexfehler i: {i_mean:.3f} ± {i_std:.3f} mgon")


# %%
def plot_error(column, title, color):
    # Plot aufsetzen
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xticks(df.index[::4])
    ax.xlimits = (0, 24)

    # Unterteilung der x-Achse in 4er-Blocks - 6 Messdurchläufe
    for x in range(0, 24, 4):
        ax.axvline(
            x=x,
            linestyle="solid",
            color="black",
            alpha=0.5,
            linewidth=2 if x == 12 else 1,
        )

    # Einzelmessfehler als Scatterplot
    df.plot(
        ax=ax,
        kind="scatter",
        x="index",
        y=column,
        color=color,
        s=100,
    )

    # Mittelwertlinie
    mean = df[column].mean()
    ax.axhline(
        y=mean,
        linestyle="solid",
        color=color,
        linewidth=2,
    )

    # Standardabweichungslinien
    std = df[column].std()
    ax.axhline(
        y=mean + std,
        linestyle="dashed",
        color=color,
        linewidth=2,
    )
    ax.axhline(
        y=mean - std,
        linestyle="dashed",
        color=color,
        linewidth=2,
    )

    ax.set_xlabel("Einzelmessung")
    ax.set_ylabel("Fehler [mgon]")
    ax.set_title(title)


plot_error("c", "Ziellinienfehler c", "red")
plt.savefig("c.png")

plot_error("i", "Indexfehler i", "blue")
plt.savefig("i.png")


# %%

import numpy as np

# restore original df
df = pd.read_csv("results.csv")
d = 5
filename = "scatter_4_6.png"

# Ausreißer entfernen
# df = df.drop(2)
# df = df.drop(df[df["index"] >= 12].index)
df = df.drop(df[df["index"] < 12].index)

# Mittelwerte für R und zeta pro Zielpunkt
mean_values = df.groupby("Zielpunkt").agg({"R": np.mean, "zeta": np.mean})

# Abweichungen jeder Einzelmessung von den Mittelwerten
dR = (df["R"] - df["Zielpunkt"].map(mean_values["R"])) * 1000
dzeta = (df["zeta"] - df["Zielpunkt"].map(mean_values["zeta"])) * 1000

# Scatterplot der Abweichungen, mit x=dR und y=dzeta
fig, ax = plt.subplots(figsize=(7, 6))
ax.set_xlabel("Abweichung R [mgon]")
ax.set_ylabel("Abweichung $\zeta$ [mgon]")
ax.axhline(y=0, color="black", linestyle="--", alpha=0.5)
ax.axvline(x=0, color="black", linestyle="--", alpha=0.5)
ax.set_xlim([-d, d])
ax.set_ylim([-d, d])

# Modify the scatter function to use different markers based on Kreislage
scatter = ax.scatter(
    dR,
    dzeta,
    s=250,
    marker="+",
    c=df["Zielpunkt"],
    cmap="Accent",
)

ax.legend(*scatter.legend_elements(), loc="lower left", title="Zielpunkt")
plt.savefig(filename)

# %%
