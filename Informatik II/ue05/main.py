import numpy as np
import matplotlib.pyplot as plt
from downloader import download, decompress

# Download files from FTP
ftp_host = "ftp.tugraz.at"
directory = "/outgoing/ITSG/teaching/2023SS_Informatik2"
download(ftp_host, directory, "key.txt")
download(ftp_host, directory, "matrix.txt.gz")

# Decompress Matrix file
decompress("matrix.txt.gz")

# Load Matrix A and Key vector k
A = np.loadtxt("matrix.txt")
k = np.loadtxt("key.txt")

# Reshape Key vector k into a column vector
k = np.reshape(k, (-1, 1))

# Decryption steps
B = A * k
K = k @ k.T
L = K + np.identity(len(k))
L_inv = np.linalg.inv(L)
C = L_inv @ B
D = C.T
E = D - L

# Plot Matrix E
fig, ax = plt.subplots()
ax.imshow(E, cmap="gray")
plt.show()
