import numpy as np
import matplotlib.pyplot as plt
from data_extraction_1 import *
from bepaling_Q1_Q2_2 import *
from ellipse_fitting_and_reshaping_3_4 import *
from arctan_Q1_Q2_5_6_7 import *
from transformatiematrix_8 import *

## First we extract all the data from the HoQI data file:

data_20260421 = Data_Extract('Data_Analysis_Part_1/20260421_HoQIs.txt')

## We use the saved Q1 and Q2 lists to import the data
unfitted_Q1_1x, unfitted_Q2_1x, unfitted_Q1_2x, unfitted_Q2_2x, unfitted_Q1_3x, unfitted_Q2_3x, unfitted_Q1_1z, unfitted_Q2_1z, unfitted_Q1_2z, unfitted_Q2_2z, unfitted_Q1_3z, unfitted_Q2_3z = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy'), np.load('Data_Analysis_Part_1/2xQ1.npy'), np.load('Data_Analysis_Part_1/2xQ2.npy'), np.load('Data_Analysis_Part_1/3xQ1.npy'), np.load('Data_Analysis_Part_1/3xQ2.npy'), np.load('Data_Analysis_Part_1/1zQ1.npy'), np.load('Data_Analysis_Part_1/1zQ2.npy'), np.load('Data_Analysis_Part_1/2zQ1.npy'), np.load('Data_Analysis_Part_1/2zQ2.npy'), np.load('Data_Analysis_Part_1/3zQ1.npy'), np.load('Data_Analysis_Part_1/3zQ2.npy')

## We then use the Q1_Q2_Length function to create the list of HoQI displacements for each

unfitted_1x, unfitted_2x, unfitted_3x, unfitted_1z, unfitted_2z, unfitted_3z = Q1_Q2_Length(unfitted_Q1_1x, unfitted_Q2_1x), Q1_Q2_Length(unfitted_Q1_2x, unfitted_Q2_2x), Q1_Q2_Length(unfitted_Q1_3x, unfitted_Q2_3x), Q1_Q2_Length(unfitted_Q1_1z, unfitted_Q2_1z), Q1_Q2_Length(unfitted_Q1_2z, unfitted_Q2_2z), Q1_Q2_Length(unfitted_Q1_3z, unfitted_Q2_3z)

## And then we use the transformation matrix to turn these into cartesian coordinates

unfitted_x, unfitted_y, unfitted_z, unfitted_Rx, unfitted_Ry, unfitted_Rz = transformatiematrix(unfitted_1x, unfitted_2x, unfitted_3x, unfitted_1z, unfitted_2z, unfitted_3z)

## And import the time axis:

time = data_20260421['T']

## And now we plot the timeseries

fig, axes = plt.subplots(2, 3)

axes[0,0].set_title('unfitted x motion timeseries')
axes[0,0].set_ylabel('motion')
axes[0,0].set_xlabel('time')
axes[0,0].plot(time, unfitted_x, ',')

axes[0,1].set_title('unfitted y motion timeseries')
axes[0,1].set_ylabel('motion')
axes[0,1].set_xlabel('time')
axes[0,1].plot(time, unfitted_y, ',')

axes[0,2].set_title('unfitted z motion timeseries')
axes[0,2].set_ylabel('motion')
axes[0,2].set_xlabel('time')
axes[0,2].plot(time, unfitted_z, ',')

axes[1,0].set_title('unfitted Rx motion timeseries')
axes[1,0].set_ylabel('motion')
axes[1,0].set_xlabel('time')
axes[1,0].plot(time, unfitted_Rx, ',')

axes[1,1].set_title('unfitted Ry motion timeseries')
axes[1,1].set_ylabel('motion')
axes[1,1].set_xlabel('time')
axes[1,1].plot(time, unfitted_Ry, ',')

axes[1,2].set_title('unfitted Rz motion timeseries')
axes[1,2].set_ylabel('motion')
axes[1,2].set_xlabel('time')
axes[1,2].plot(time, unfitted_Rz, ',')

plt.subplots_adjust(hspace=0.312, wspace=0.312)
plt.show()