# BEGIN: ed8c6549bwf9
# Scatterplot der Abweichungen, mit x=dR und y=dzeta
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(dR, dzeta, s=100)
ax.set_xlabel("Abweichung R [mgon]")
ax.set_ylabel("Abweichung zeta [mgon]")
ax.axhline(y=0, color="black", linestyle="--")
ax.axvline(x=0, color="black", linestyle="--")
ax.set_xlim([-0.05, 0.05])
ax.set_ylim([-0.05, 0.05])
# END: ed8c6549bwf9
