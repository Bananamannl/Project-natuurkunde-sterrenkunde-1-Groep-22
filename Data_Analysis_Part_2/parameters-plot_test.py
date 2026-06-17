import numpy as np
import matplotlib.pyplot as plt
from find_windows_interactive import *
from ellipse_parameters import *

Q1, Q2  = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ2.npy")
parms_1z = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\param_timeseries_1z_step_size_10_window_size_500.npy")
max_x, max_y, max_a, max_b, max_theta = np.max(parms_1z, axis=0)
a = parms_1z[:, 2]

print(max_x, max_y, max_a, max_b, max_theta)

Q1, Q2 = Q1[:1829000], Q2[:1829000]

params = parameters_timeseries_interactive(Q1, Q2, window_size=250, step_size=250)
x0 = params[7314, 0]
y0 = params[7314, 1]
a = params[7314, 2]
b = params[7314, 3]
theta = params[7314, 4]


Q1, Q2 = Q1[1828500:1828750], Q2[1828500:1828750]

t = np.linspace(0, 2*np.pi, 500)

x = a * np.cos(t)
y = b * np.sin(t)

xr = x*np.cos(theta) - y*np.sin(theta)
yr = x*np.sin(theta) + y*np.cos(theta)

xr += x0
yr += y0

a, b = parms_1z[:, 2], parms_1z[:, 3]

# plt.plot(a)
# plt.plot(b)
plt.plot(xr, yr)
plt.axis("equal")
plt.scatter(Q1, Q2)
plt.show()

