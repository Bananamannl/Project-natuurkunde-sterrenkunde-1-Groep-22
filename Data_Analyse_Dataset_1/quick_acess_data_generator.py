import numpy as np
from ellipse_fitting_and_reshaping_3_4 import *
from arctan_Q1_Q2_5_6_7 import *
from transformatiematrix_8 import *

unfitted_Q1_1x, unfitted_Q2_1x, unfitted_Q1_2x, unfitted_Q2_2x, unfitted_Q1_3x, unfitted_Q2_3x, unfitted_Q1_1z, unfitted_Q2_1z, unfitted_Q1_2z, unfitted_Q2_2z, unfitted_Q1_3z, unfitted_Q2_3z = np.load('Data_Analyse_Dataset_1/1xQ1.npy'), np.load('Data_Analyse_Dataset_1/1xQ2.npy'), np.load('Data_Analyse_Dataset_1/2xQ1.npy'), np.load('Data_Analyse_Dataset_1/2xQ2.npy'), np.load('Data_Analyse_Dataset_1/3xQ1.npy'), np.load('Data_Analyse_Dataset_1/3xQ2.npy'), np.load('Data_Analyse_Dataset_1/1zQ1.npy'), np.load('Data_Analyse_Dataset_1/1zQ2.npy'), np.load('Data_Analyse_Dataset_1/2zQ1.npy'), np.load('Data_Analyse_Dataset_1/2zQ2.npy'), np.load('Data_Analyse_Dataset_1/3zQ1.npy'), np.load('Data_Analyse_Dataset_1/3zQ2.npy')

fitted_Q1_1x, fitted_Q2_1x = transform(unfitted_Q1_1x, unfitted_Q2_1x)
fitted_Q1_2x, fitted_Q2_2x = transform(unfitted_Q1_2x, unfitted_Q2_2x)
fitted_Q1_3x, fitted_Q2_3x = transform(unfitted_Q1_3x, unfitted_Q2_3x) 
fitted_Q1_1z, fitted_Q2_1z = transform(unfitted_Q1_1z, unfitted_Q2_1z)
fitted_Q1_2z, fitted_Q2_2z = transform(unfitted_Q1_2z, unfitted_Q2_2z)
fitted_Q1_3z, fitted_Q2_3z = transform(unfitted_Q1_3z, unfitted_Q2_3z)

fitted_1x, fitted_2x, fitted_3x, fitted_1z, fitted_2z, fitted_3z = Q1_Q2_Length(fitted_Q1_1x, fitted_Q2_1x), Q1_Q2_Length(fitted_Q1_2x, fitted_Q2_2x), Q1_Q2_Length(fitted_Q1_3x, fitted_Q2_3x), Q1_Q2_Length(fitted_Q1_1z, fitted_Q2_1z), Q1_Q2_Length(fitted_Q1_2z, fitted_Q2_2z), Q1_Q2_Length(fitted_Q1_3z, fitted_Q2_3z)

fitted_x, fitted_y, fitted_z, fitted_Rx, fitted_Ry, fitted_Rz = transformatiematrix(fitted_1x, fitted_2x, fitted_3x, fitted_1z, fitted_2z, fitted_3z)

## Creating a quickacces file for the coordinates
# uncomment these by slecting and pressing ctrl + /, then run, then re-comment

# HoQI_six_vct_list = []
# for i in range(0, len(fitted_1x)):
#     six_vct = np.array([fitted_1x[i], fitted_2x[i], fitted_3x[i], fitted_1z[i], fitted_2z[i], fitted_3z[i]])
#     HoQI_six_vct_list.append(six_vct)

# HoQI_six_vct_list = np.squeeze(np.array(HoQI_six_vct_list))

# np.save('Data_Analyse_Dataset_1/HoQI_fitted_six_vct_list.npy', HoQI_six_vct_list)

# six_vct_list = []
# for i in range(0, len(fitted_x)):
#     six_vct = np.array([fitted_x[i], fitted_y[i], fitted_z[i], fitted_Rx[i], fitted_Ry[i], fitted_Rz[i]])
#     six_vct_list.append(six_vct)

# six_vct_list = np.squeeze(np.array(six_vct_list))

# np.save('Data_Analyse_Dataset_1/fitted_six_vct_list.npy', six_vct_list)