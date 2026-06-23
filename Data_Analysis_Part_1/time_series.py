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

## We then use the ellipse fitting to adjust this data
fitted_Q1_1x, fitted_Q2_1x = transform(unfitted_Q1_1x, unfitted_Q2_1x)
fitted_Q1_2x, fitted_Q2_2x = transform(unfitted_Q1_2x, unfitted_Q2_2x)
fitted_Q1_3x, fitted_Q2_3x = transform(unfitted_Q1_3x, unfitted_Q2_3x) 
fitted_Q1_1z, fitted_Q2_1z = transform(unfitted_Q1_1z, unfitted_Q2_1z)
fitted_Q1_2z, fitted_Q2_2z = transform(unfitted_Q1_2z, unfitted_Q2_2z)
fitted_Q1_3z, fitted_Q2_3z = transform(unfitted_Q1_3z, unfitted_Q2_3z)

## We then use both these data sets and the Q1_Q2_Length function to create the list of HoQI displacements for each
unfitted_1x, unfitted_2x, unfitted_3x, unfitted_1z, unfitted_2z, unfitted_3z = Q1_Q2_Length(unfitted_Q1_1x, unfitted_Q2_1x), Q1_Q2_Length(unfitted_Q1_2x, unfitted_Q2_2x), Q1_Q2_Length(unfitted_Q1_3x, unfitted_Q2_3x), Q1_Q2_Length(unfitted_Q1_1z, unfitted_Q2_1z), Q1_Q2_Length(unfitted_Q1_2z, unfitted_Q2_2z), Q1_Q2_Length(unfitted_Q1_3z, unfitted_Q2_3z)

fitted_1x, fitted_2x, fitted_3x, fitted_1z, fitted_2z, fitted_3z = Q1_Q2_Length(fitted_Q1_1x, fitted_Q2_1x), Q1_Q2_Length(fitted_Q1_2x, fitted_Q2_2x), Q1_Q2_Length(fitted_Q1_3x, fitted_Q2_3x), Q1_Q2_Length(fitted_Q1_1z, fitted_Q2_1z), Q1_Q2_Length(fitted_Q1_2z, fitted_Q2_2z), Q1_Q2_Length(fitted_Q1_3z, fitted_Q2_3z)

## And then we use the tranformationmatrix to turn these into cartesian coordinates
unfitted_x, unfitted_y, unfitted_z, unfitted_Rx, unfitted_Ry, unfitted_Rz = transformatiematrix(unfitted_1x, unfitted_2x, unfitted_3x, unfitted_1z, unfitted_2z, unfitted_3z)

fitted_x, fitted_y, fitted_z, fitted_Rx, fitted_Ry, fitted_Rz = transformatiematrix(fitted_1x, fitted_2x, fitted_3x, fitted_1z, fitted_2z, fitted_3z)

## And import the ones from the HoQI file, as well as the time axis:
time = data_20260421['T']

data_x, data_y, data_z, data_Rx, data_Ry, data_Rz = data_20260421['RM_HOQI_X'], data_20260421['RM_HOQI_Y'], data_20260421['RM_HOQI_Z'], data_20260421['RM_HOQI_RX'], data_20260421['RM_HOQI_RY'], data_20260421['RM_HOQI_RZ']

## And now we plot the timeseries
fig, axes = plt.subplots(3, 1)
axes[0].set_title('unfitted z motion timeseries')
axes[0].set_ylabel('motion')
axes[0].set_xlabel('time')
axes[0].plot(time, unfitted_z, ',')
axes[1].set_title('fitted z motion timeseries')
axes[1].set_ylabel('motion')
axes[1].set_xlabel('time')
axes[1].plot(time, fitted_z, ',')
axes[2].set_title('data z motion timeseries')
axes[2].set_ylabel('motion')
axes[2].set_xlabel('time')
axes[2].plot(time, data_z, ',')

plt.subplots_adjust(hspace=0.312)
plt.show()