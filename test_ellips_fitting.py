from ellips_fitting_and_reshaping_3_4 import transform
import numpy as np
import matplotlib.pyplot as plt

Q1 = np.load("1xQ1.npy")
Q2 = np.load("1xQ2.npy")
Q1_new, Q2_new = transform(Q1, Q2)

plt.figure()
# plt.scatter(Q1[0:1000], Q2[0:1000], s=3)
# plt.scatter(Q1, Q2, s=3)
plt.scatter(Q1_new, Q2_new, s=3)
plt.axis("equal") 
plt.grid()
plt.show()