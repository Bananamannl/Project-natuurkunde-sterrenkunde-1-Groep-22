from functions import *
from ellipse_parameters import parameters_timeseries
import matplotlib.pyplot as plt

Q1, Q2 = np.load("Data_Analyse_Dataset_1\\1zQ1.npy"), np.load("Data_Analyse_Dataset_1\\1zQ2.npy")
Q1, Q2 = transform(Q1[:2860], Q2[:2860])

paramaters = parameters_timeseries(Q1, Q2, window_size=100, step_size=5)
parameters = paramaters - paramaters.mean(axis=0)

data = parameters[:, :3] * 100

# plt.plot(paramaters)
# plt.legend(["x0", "y0", "theta", "a", "b", "area"])
# plt.show()

plt.plot(data)
plt.legend(["x0", "y0", "a"])
plt.show()