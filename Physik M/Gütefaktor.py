import numpy as np

data = np.loadtxt("Gütefaktor.txt")

w = data[:, 0]
A = data[:, 1]

# find w where A is max (natural frequency)
w_max = w[np.argmax(A)]

# calculate the half-power width
dw = 2 * abs(w_max - w[np.argmin(np.abs(A - 0.5 * np.max(A)))])

Q = abs(w_max / dw)

print(w_max)
print(Q)
