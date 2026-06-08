import numpy as np

from ellipse_fitting_and_reshaping_3_4 import transform
from arctan_Q1_Q2_5_6_7 import Q1_Q2_Length
from transformatiematrix_8 import transformatiematrix

# aanhalen van de matrix met alle zesvectoren:
zesvector_matrix = np.load("Data_Analyse_Dataset_1/fitted_six_vct_list.npy")

# aanmaken van de benodigde snelheidslijsten:
velocity_x, velocity_y, velocity_z, velocity_Rx, velocity_Ry, velocity_Rz, velocity_x_gefit, velocity_y_gefit, velocity_z_gefit, velocity_Rx_gefit, velocity_Ry_gefit, velocity_Rz_gefit = [[] for j in range(12)]

# aanhalen van de benodigde verplaatsingslijsten:
# extracting the Q lists from the saved data files to prevent Python from having to read all the raw data first
Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('Data_Analyse_Dataset_1/1xQ1.npy'), np.load('Data_Analyse_Dataset_1/1xQ2.npy'), np.load('Data_Analyse_Dataset_1/2xQ1.npy'), np.load('Data_Analyse_Dataset_1/2xQ2.npy'), np.load('Data_Analyse_Dataset_1/3xQ1.npy'), np.load('Data_Analyse_Dataset_1/3xQ2.npy'), np.load('Data_Analyse_Dataset_1/1zQ1.npy'), np.load('Data_Analyse_Dataset_1/1zQ2.npy'), np.load('Data_Analyse_Dataset_1/2zQ1.npy'), np.load('Data_Analyse_Dataset_1/2zQ2.npy'), np.load('Data_Analyse_Dataset_1/3zQ1.npy'), np.load('Data_Analyse_Dataset_1/3zQ2.npy')

# note: some of these lists contain minus signs due to the polarization plate being turned in the oppositie direction in the original experiment
length_1x_lijst = -Q1_Q2_Length(Q1_1x, Q2_1x)

length_2x_lijst = Q1_Q2_Length(Q1_2x, Q2_2x)

length_3x_lijst = Q1_Q2_Length(Q1_3x, Q2_3x)

length_1z_lijst = -Q1_Q2_Length(Q1_1z, Q2_1z)

length_2z_lijst = -Q1_Q2_Length(Q1_2z, Q2_2z)

length_3z_lijst = -Q1_Q2_Length(Q1_3z, Q2_3z)

# de lijsten met de werkelijke verplaatsingen in alle zes de vrijheidsgraden:
x_lijst, y_lijst, z_lijst, Rx_lijst, Ry_lijst, Rz_lijst  = transformatiematrix(length_1x_lijst, length_2x_lijst, length_3x_lijst, length_1z_lijst, length_2z_lijst, length_3z_lijst)
x_lijst_gefit = zesvector_matrix[0:int(3e6), 0]
y_lijst_gefit = zesvector_matrix[0:int(3e6), 1]
z_lijst_gefit = zesvector_matrix[0:int(3e6), 2]
Rx_lijst_gefit = zesvector_matrix[0:int(3e6), 3]
Ry_lijst_gefit = zesvector_matrix[0:int(3e6), 4]
Rz_lijst_gefit = zesvector_matrix[0:int(3e6), 5]

for i in range(0, len(x_lijst)-1):
    v_x = (x_lijst[i+1] - x_lijst[i])/0.001
    v_y = (y_lijst[i+1] - y_lijst[i])/0.001
    v_z = (z_lijst[i+1] - z_lijst[i])/0.001
    v_Rx = (Rx_lijst[i+1] - Rx_lijst[i])/0.001
    v_Ry = (Ry_lijst[i+1] - Ry_lijst[i])/0.001
    v_Rz = (Rz_lijst[i+1] - Rz_lijst[i])/0.001
    v_x_gefit = (x_lijst_gefit[i+1] - x_lijst_gefit[i])/0.001
    v_y_gefit = (y_lijst_gefit[i+1] - y_lijst_gefit[i])/0.001
    v_z_gefit = (z_lijst_gefit[i+1] - z_lijst_gefit[i])/0.001
    v_Rx_gefit = (Rx_lijst_gefit[i+1] - Rx_lijst_gefit[i])/0.001
    v_Ry_gefit = (Ry_lijst_gefit[i+1] - Ry_lijst_gefit[i])/0.001
    v_Rz_gefit = (Rz_lijst_gefit[i+1] - Rz_lijst_gefit[i])/0.001

    velocity_x.append(v_x)
    velocity_y.append(v_y)
    velocity_z.append(v_z)
    velocity_Rx.append(v_Rx)
    velocity_Ry.append(v_Ry)
    velocity_Rz.append(v_Rz)
    velocity_x_gefit.append(v_x_gefit)
    velocity_y_gefit.append(v_y_gefit)
    velocity_z_gefit.append(v_z_gefit)
    velocity_Rx_gefit.append(v_Rx_gefit)
    velocity_Ry_gefit.append(v_Ry_gefit)
    velocity_Rz_gefit.append(v_Rz_gefit)

# print statement as a quick test
print([float(v_x) for v_x in velocity_x])