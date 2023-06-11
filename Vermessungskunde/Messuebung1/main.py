# %%
"Vorprozessierung"

import pandas as pd
import matplotlib.pyplot as plt

# Messdaten einlesen
df = pd.read_csv("data.csv")

# In der Tabelle sind die Kreislagen 1 und 2 als eigene Zeilen jeweils
# im Wechsel angeordnet. Zuerst müssen diese Messungen in ein Zeile
# zusammengefasst werden.
K1 = df[::2].reset_index(drop=True)
K2 = df[1::2].reset_index(drop=True)

df = pd.DataFrame(
    {
        "index": range(0, 24),
        "Satz": K1["Satz"],
        "Beobachter": K1["Beobachter"],
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


# c und i in [cc] umrechnen
df["c"] = 10000 * df["c"]
df["i"] = 10000 * df["i"]

# Ergebnisse speichern
df.to_csv("results.csv", index=False)

# %%
"Tabelle aller Abweichungen"


def as_typst_table(rows: list[dict]) -> str:
    """
    Format data as a table in Typst format.
    :param rows: List of dicts with the same keys.
    """
    columns = rows[0].keys()
    lines = [
        "#table(",
        f"  columns: {len(columns)},",
        "  " + ",".join([f"[*{key}*]" for key in columns]) + ",",
    ]
    for row in rows:
        lines += ["  " + ",".join([f"[{value}]" for value in row.values()]) + ","]
    lines += ")"
    return "\n".join(lines)


def format_errors(df):
    return as_typst_table(
        [
            {
                "Satz": row["Satz"],
                "Zielpunkt": row["Zielpunkt"],
                "c [cc]": int(row["c"]),
                "i [cc]": int(row["i"]),
            }
            for _, row in df.iterrows()
        ]
        + [
            {
                "Satz": "*Mittelwert*",
                "Zielpunkt": "",
                "c [cc]": int(df["c"].mean()),
                "i [cc]": int(df["i"].mean()),
            },
            {
                "Satz": "*Standardabweichung*",
                "Zielpunkt": "",
                "c [cc]": int(df["c"].std(ddof=1)),
                "i [cc]": int(df["i"].std(ddof=1)),
            },
        ]
    )


print(format_errors(df[df["Satz"] <= 3]))
print(format_errors(df[df["Satz"] > 3]))


# %%
"Tabellen der Mittelwerte"


def format_means(df):
    return as_typst_table(
        [
            {
                "Zielpunkt": row["Zielpunkt"],
                "Satz": row["Satz"],
                "R [gon]": round(row["R"], 3),
                "zeta [gon]": round(row["zeta"], 3),
            }
            for _, row in df.iterrows()
        ]
    )


df = df.sort_values(by=["Zielpunkt", "Satz"])
print(format_means(df[df["Satz"] <= 3]))
print(format_means(df[df["Satz"] > 3]))

# %%
"Horizontalfehler Plots"

zielpunkte = [1, 2, 3, 4]
beobachter = ["Juliane Medl", "Daniel Ebert"]


def plot_error(column, ylabel, filename):
    fig, ax = plt.subplots(figsize=(8, 4))

    mean = df[column].mean()

    for z in zielpunkte:
        y1 = df[(df["Zielpunkt"] == z) & (df["Beobachter"] == beobachter[0])][column]
        y2 = df[(df["Zielpunkt"] == z) & (df["Beobachter"] == beobachter[1])][column]

        width = 1 / 10

        ax.bar(
            [
                z - width * 2.5,
                z - width * 1.5,
                z - width * 0.5,
            ],
            y1 - mean,
            width * 0.9,
            color="purple",
            bottom=mean,
        )
        ax.bar(
            [
                z + width * 0.5,
                z + width * 1.5,
                z + width * 2.5,
            ],
            y2 - mean,
            width * 0.9,
            color="green",
            bottom=mean,
        )
    ax.legend(beobachter)
    ax.axhline(y=mean, linestyle="--", color="gray")
    ax.set_xticks(zielpunkte)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Zielpunkt")
    fig.savefig(filename, dpi=300)


plot_error("c", "Ziellinienfehler c [cc]", "c.png")
plot_error("i", "Indexfehler i [cc]", "i.png")

# %%
"Kreislagenmittel Plots"

fig, axs = plt.subplots(2, 2, figsize=(12, 12))

# get the mean of R and zeta for each Zielpunkt. Ignore all other columms
mean_values = df.groupby("Zielpunkt")[["R", "zeta"]].mean()

for i, z in enumerate(zielpunkte):
    R = mean_values.loc[z, "R"]
    zeta = mean_values.loc[z, "zeta"]
    d = 0.1
    R = round(R, 1)
    zeta = round(zeta, 1)

    ax = axs[i // 2, i % 2]
    ax.set_title(f"Zielpunkt {z}")
    ax.set_aspect("equal")

    xmin, xmax = R - d, R + d
    ax.set_xlabel("R [gon]")
    ax.set_xlim(xmin, xmax)
    ax.set_xticks([xmin, xmax])

    ymin, ymax = zeta - d, zeta + d
    ax.set_ylabel("$\zeta$ [gon]")
    ax.set_ylim(ymin, ymax)
    ax.set_yticks([ymin, ymax])

    data1 = df[(df["Zielpunkt"] == z) & (df["Beobachter"] == beobachter[0])]
    data2 = df[(df["Zielpunkt"] == z) & (df["Beobachter"] == beobachter[1])]

    ax.scatter(
        data1["R"],
        data1["zeta"],
        color="purple",
        marker="+",
        s=200,
    )
    ax.scatter(
        data2["R"],
        data2["zeta"],
        color="green",
        marker="+",
        s=200,
    )

    if i == 1:
        ax.legend(beobachter)

fig.savefig("Kreislagenmittel.png", dpi=300)
