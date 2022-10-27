import matplotlib.pyplot as plt

plt.axis("off")

A = (20, 20)
B = (80, 10)
C = (80, 80)


# A-B
plt.plot([A[0], B[0]], [A[1], B[1]], color="red")

# B-C
plt.plot([B[0], C[0]], [B[1], C[1]], color="red")

# C-A
plt.plot([C[0], A[0]], [C[1], A[1]], color="red")


# A
plt.scatter(x=A[0], y=A[1], marker="x", color="red", s=2)
plt.annotate("A", (A[0] - 3, A[1] - 1), color="red")

# # B
# plt.scatter(B[0], B[1], marker="x", color="red", linewidths=2)
# plt.annotate("B", (B[0] + 2, B[1] - 1.5), color="red")

# # C
# plt.scatter(C[0], C[1], marker="x", color="red", linewidths=2)
# plt.annotate("C", (C[0], C[1] + 2), color="red")

plt.savefig("result.png")


# p = Plot((0, 100), (0, 100))

# A = CartesianCoordinate(20, 20)
# B = CartesianCoordinate(80, 10)
# C = CartesianCoordinate(70, 80)

# p.add_known_point(A)
# p.add_known_point(B)
# p.add_known_point(C)

# p.save("result.png")
