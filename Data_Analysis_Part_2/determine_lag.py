import numpy as np
from ellipse_parameters import *
from functions import *
import matplotlib.pyplot as plt

HoQIs, Q1, Q2 = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy"), np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")
# Q1, Q2 = transform(Q1[0:10000], Q2[0:10000])
Q1, Q2 = (Q1[20000:21500], Q2[20000:21500])
parameters = parameters_timeseries(Q1, Q2, window_size=100, step_size=1) #1401 windows


a, b = parameters[:, 0], parameters[:, 1] #dus een lijst met 1401 getallen
a = (a - np.mean(a)) * 20
b = (b - np.mean(b)) * 20
def norm(Q1, Q2):
    """
    A function that finds the norm of every Q vector
    """
    norms = np.sqrt(Q1 **2 + Q2 ** 2)
    norms = norms - np.mean(norms)
    return norms
norms = norm(Q1, Q2)

# plt.plot(lijst, a, label='a')
# plt.plot(lijst, b, label='b')
# plt.plot(norms, label='norms')
# plt.legend(fontsize=12, loc = 'upper right')
# plt.show()

corr_lijst = []
#Conclusie, gebruik gewoon lag=0
for i in range(100):
    # print("lag=", i, "geeft:")
    # print(np.corrcoef(norms[i:1401+i], b)[1, 0])
    corr_lijst.append(np.corrcoef(norms[i:1401+i], b)[1, 0])

hoogste_waarde = max(corr_lijst)
index = corr_lijst.index(hoogste_waarde)

print("Hoogste waarde:", hoogste_waarde)
print("Index:", index)