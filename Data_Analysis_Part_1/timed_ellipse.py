import matplotlib.pyplot as plt
import numpy as np
from ellipse_fitting_and_reshaping_3_4 import *

# Import all the Q1 and Q2
Q1_list = [np.load('Data_Analysis_Part_1/1xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/2xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/3xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/1zQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/2zQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/3zQ1.npy')[:3000000]]

Q2_list = [np.load('Data_Analysis_Part_1/1xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/2xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/3xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/1zQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/2zQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/3zQ2.npy')[:3000000]]

Q1_transformed = [0]*6
Q2_transformed = [0]*6
for h in range(0,6):
    fitted_Q1, fitted_Q2 = transform(Q1_list[h], Q2_list[h])
    Q1_transformed[h] = fitted_Q1
    Q2_transformed[h] = fitted_Q2


names_list = ['1x', '2x', '3x', '1z', '2z', '3z']

# Make a plot of all the ellipses on top of eachother
figure, axes = plt.subplots(2, 3)
for i in range(0,2):
    for j in range(0,3):
        axes[i, j].set_ylabel('Q2')
        axes[i, j].set_xlabel('Q1')
        axes[i, j].plot(Q1_list[i*3+j], Q2_list[i*3+j], ',')
        axes[i, j].set_title(names_list[i*3+j])

figure.tight_layout()
plt.subplots_adjust(hspace=0.312, wspace=0.4)
plt.show()

figure, axes = plt.subplots(2, 3)
for i in range(0,2):
    for j in range(0,3):
        axes[i, j].set_ylabel('Q2')
        axes[i, j].set_xlabel('Q1')
        axes[i, j].plot(Q1_transformed[i*3+j], Q2_transformed[i*3+j], ',r')
        axes[i, j].set_title(names_list[i*3+j])
        axes[i, j].set_xlim(-1.43, 1.43)

figure.tight_layout()
plt.subplots_adjust(hspace=0.312, wspace=0.4)
plt.show()