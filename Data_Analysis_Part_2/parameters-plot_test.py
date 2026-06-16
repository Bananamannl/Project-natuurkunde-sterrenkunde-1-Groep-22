import numpy as np
import matplotlib.pyplot as plt
from ellipse_parameters import *

Q1, Q2  = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1zQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1zQ2.npy")
parms_1z = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\param_timeseries_1z_step_size_10_window_size_500.npy")
max_x, max_y, max_a, max_b, max_theta = np.max(parms_1z, axis=0)
a = parms_1z[:, 2]

print(max_x, max_y, max_a, max_b, max_theta)

Q1, Q2 = Q1[616968:617218], Q2[616968:617218]

params = parameters(Q1, Q2)[0]
x0 = params[:, 0]
y0 = params[:, 1]
a = params[:, 2]
b = params[:, 3]
theta = params[:, 4]
# print("vector:", np.hstack(x0, y0, a, b, theta))
# plt.plot(a)

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
# plt.plot(xr, yr)
# plt.axis("equal")
plt.scatter(Q1, Q2)
plt.show()

