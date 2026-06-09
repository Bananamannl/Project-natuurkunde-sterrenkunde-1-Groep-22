from functies import *
from ellipse_parameters import *
import matplotlib.pyplot as plt

Q1, Q2 = np.load("Data_Analyse_Dataset_1\\1zQ1.npy"), np.load("Data_Analyse_Dataset_1\\1zQ2.npy")
Q1, Q2 = transform(Q1[:1430], Q2[:1430])

paramaters = parameters_timeseries(Q1, Q2, window_size=100, step_size=50)

plt.plot(paramaters)
plt.legend(["x0", "y0", "theta", "a", "b", "area"])
plt.show()