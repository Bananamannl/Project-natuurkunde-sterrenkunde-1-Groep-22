# importing the necessary libraries and functions 
import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from functions import *
from frequency_dependent_smoothing import *

# introducing some important variables
segment_time_set = 1000
fs_set = 1000

window_size_1x_2x = 500
window_size_3x = 210
window_size_1z_2z_3z = 250

# extracting the Q lists from the np.saves to prevent Python from having to read the raw data file first
Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy'), np.load('Data_Analysis_Part_1/2xQ1.npy'), np.load('Data_Analysis_Part_1/2xQ2.npy'), np.load('Data_Analysis_Part_1/3xQ1.npy'), np.load('Data_Analysis_Part_1/3xQ2.npy'), np.load('Data_Analysis_Part_1/1zQ1.npy'), np.load('Data_Analysis_Part_1/1zQ2.npy'), np.load('Data_Analysis_Part_1/2zQ1.npy'), np.load('Data_Analysis_Part_1/2zQ2.npy'), np.load('Data_Analysis_Part_1/3zQ1.npy'), np.load('Data_Analysis_Part_1/3zQ2.npy')

# transforming the Q lists with single ellipse fitting
Q1_1x_single, Q2_1x_single = transform(Q1_1x, Q2_1x)
Q1_2x_single, Q2_2x_single = transform(Q1_2x, Q2_2x)
Q1_3x_single, Q2_3x_single = transform(Q1_3x, Q2_3x)
Q1_1z_single, Q2_1z_single = transform(Q1_1z, Q2_1z)
Q1_2z_single, Q2_2z_single = transform(Q1_2z, Q2_2z)
Q1_3z_single, Q2_3z_single = transform(Q1_3z, Q2_3z)

# transforming the Q lists with windowed ellipse fitting
Q1_1x_windowed, Q2_1x_windowed = standard_step_window_ellipse_fitting(Q1_1x, Q2_1x, window_size_1x_2x)
Q1_2x_windowed, Q2_2x_windowed = standard_step_window_ellipse_fitting(Q1_2x, Q2_2x, window_size_1x_2x)
Q1_3x_windowed, Q2_3x_windowed = standard_step_window_ellipse_fitting(Q1_3x, Q2_3x, window_size_3x)
Q1_1z_windowed, Q2_1z_windowed = standard_step_window_ellipse_fitting(Q1_1z, Q2_1z, window_size_1z_2z_3z)
Q1_2z_windowed, Q2_2z_windowed = standard_step_window_ellipse_fitting(Q1_2z, Q2_2z, window_size_1z_2z_3z)
Q1_3z_windowed, Q2_3z_windowed = standard_step_window_ellipse_fitting(Q1_3z, Q2_3z, window_size_1z_2z_3z)

# note: some of the undermentioned lists contain a minus sign due to the polarization plate being turned in the oppositie direction in the original experiment
# calculating the HoQI displacements (so NOT the displacements in the six degrees of freedom) using the above derived Q lists
length_1x_list = -Q1_Q2_Length(Q1_1x, Q2_1x)
length_2x_list = Q1_Q2_Length(Q1_2x, Q2_2x)
length_3x_list = Q1_Q2_Length(Q1_3x, Q2_3x)
length_1z_list = -Q1_Q2_Length(Q1_1z, Q2_1z)
length_2z_list = -Q1_Q2_Length(Q1_2z, Q2_2z)
length_3z_list = -Q1_Q2_Length(Q1_3z, Q2_3z)

# calculating the HoQI displacements (so NOT the displacements in the six degrees of freedom) using the above derived single ellipse fitted Q lists
length_1x_list_single = -Q1_Q2_Length(Q1_1x_single, Q2_1x_single)
length_2x_list_single = Q1_Q2_Length(Q1_2x_single, Q2_2x_single)
length_3x_list_single = Q1_Q2_Length(Q1_3x_single, Q2_3x_single)
length_1z_list_single = -Q1_Q2_Length(Q1_1z_single, Q2_1z_single)
length_2z_list_single = -Q1_Q2_Length(Q1_2z_single, Q2_2z_single)
length_3z_list_single = -Q1_Q2_Length(Q1_3z_single, Q2_3z_single)

# calculating the HoQI displacements (so NOT the displacements in the six degrees of freedom) using the above derived windowed ellipse fitted Q lists
# note: we removed the last 150 elements of the 1x, 2x, 1z, 2z, and 3z lists to make those lists the same length as the 3x list, of which the last 150 elements got removed automatically in the standard_step_window_ellipse_fitting function (since window_size_3x = 210 and 3,000,000 mod 210 ≡ 150)
length_1x_list_windowed = -Q1_Q2_Length(Q1_1x_windowed, Q2_1x_windowed)[:-150]
length_2x_list_windowed = Q1_Q2_Length(Q1_2x_windowed, Q2_2x_windowed)[:-150]
length_3x_list_windowed = Q1_Q2_Length(Q1_3x_windowed, Q2_3x_windowed)
length_1z_list_windowed = -Q1_Q2_Length(Q1_1z_windowed, Q2_1z_windowed)[:-150]
length_2z_list_windowed = -Q1_Q2_Length(Q1_2z_windowed, Q2_2z_windowed)[:-150]
length_3z_list_windowed = -Q1_Q2_Length(Q1_3z_windowed, Q2_3z_windowed)[:-150]

# calculating the actual displacements of the center of mass in all six degrees of freedom
x_list, y_list, z_list, Rx_list, Ry_list, Rz_list  = transformatiematrix(length_1x_list, length_2x_list, length_3x_list, length_1z_list, length_2z_list, length_3z_list)
x_list_single, y_list_single, z_list_single, Rx_list_single, Ry_list_single, Rz_list_single  = transformatiematrix(length_1x_list_single, length_2x_list_single, length_3x_list_single, length_1z_list_single, length_2z_list_single, length_3z_list_single)
x_list_windowed, y_list_windowed, z_list_windowed, Rx_list_windowed, Ry_list_windowed, Rz_list_windowed  = transformatiematrix(length_1x_list_windowed, length_2x_list_windowed, length_3x_list_windowed, length_1z_list_windowed, length_2z_list_windowed, length_3z_list_windowed)

# extracting the raw data file to bring in the displacements derived by the initial data analysis of the research group  
data_20260421 = Data_Extract('Data_Analysis_Part_1/20260421_HoQIs.txt')

# putting the HoQI displacements of the raw data file in lists
length_1x_list_dataset = data_20260421["SENS_HOQI_1_H_DISP_LEN"]
length_2x_list_dataset = data_20260421["SENS_HOQI_2_H_DISP_LEN"]
length_3x_list_dataset = data_20260421["SENS_HOQI_3_H_DISP_LEN"]
length_1z_list_dataset = data_20260421["SENS_HOQI_1_V_DISP_LEN"]
length_2z_list_dataset = data_20260421["SENS_HOQI_2_V_DISP_LEN"]
length_3z_list_dataset = data_20260421["SENS_HOQI_3_V_DISP_LEN"]

# putting the DoF (i.e.: degrees of freedom) displacements of the raw data file in lists
x_list_dataset = data_20260421["RM_HOQI_X"] 
y_list_dataset = data_20260421["RM_HOQI_Y"] 
z_list_dataset = data_20260421["RM_HOQI_Z"] 
Rx_list_dataset = data_20260421["RM_HOQI_RX"] 
Ry_list_dataset = data_20260421["RM_HOQI_RY"] 
Rz_list_dataset = data_20260421["RM_HOQI_RZ"] 

# segment time: any outliers caused by noise are averaged out by dividing the data into several segments and applying the frequency dependent smoothing function defined in the eponymous code file
# defining the different raw (so the non-smoothened) ASD's for the displacements in all six degrees of freedom
gwpy = get_asd(x_list, fs_set, segment_time_set); asd_x_raw, f_x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(y_list, fs_set, segment_time_set); asd_y_raw, f_y_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(z_list, fs_set, segment_time_set); asd_z_raw, f_z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rx_list, fs_set, segment_time_set); asd_Rx_raw, f_Rx_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Ry_list, fs_set, segment_time_set); asd_Ry_raw, f_Ry_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rz_list, fs_set, segment_time_set); asd_Rz_raw, f_Rz_raw = gwpy.value, gwpy.frequencies.value

# defining the different smoothened ASD's for the displacement in all six degrees of freedom
# both the value of 'log_step' and the value of 'n_ave' are adopted from the Python file titled 'frequency_dependent_smoothing.py'
asd_x, f_x = asd_smooth(asd_x_raw, f_x_raw, log_step=8, n_ave=2)
asd_y, f_y = asd_smooth(asd_y_raw, f_y_raw, log_step=8, n_ave=2)
asd_z, f_z = asd_smooth(asd_z_raw, f_z_raw, log_step=8, n_ave=2)
asd_Rx, f_Rx = asd_smooth(asd_Rx_raw, f_Rx_raw, log_step=8, n_ave=2)
asd_Ry, f_Ry = asd_smooth(asd_Ry_raw, f_Ry_raw, log_step=8, n_ave=2)
asd_Rz, f_Rz = asd_smooth(asd_Rz_raw, f_Rz_raw, log_step=8, n_ave=2)

# defining the different raw (so the non-smoothened) ASD's for the direct HoQI displacements
gwpy = get_asd(length_1x_list, fs_set, segment_time_set); asd_1x_raw, f_1x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2x_list, fs_set, segment_time_set); asd_2x_raw, f_2x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3x_list, fs_set, segment_time_set); asd_3x_raw, f_3x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_1z_list, fs_set, segment_time_set); asd_1z_raw, f_1z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2z_list, fs_set, segment_time_set); asd_2z_raw, f_2z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3z_list, fs_set, segment_time_set); asd_3z_raw, f_3z_raw = gwpy.value, gwpy.frequencies.value

# defining the different smoothened ASD's for the direct HoQI displacements
# once again, both the value of 'log_step' and the value of 'n_ave' are adopted from the Python file titled 'frequency_dependent_smoothing.py'
asd_1x, f_1x = asd_smooth(asd_1x_raw, f_1x_raw, log_step=8, n_ave=2)
asd_2x, f_2x = asd_smooth(asd_2x_raw, f_2x_raw, log_step=8, n_ave=2)
asd_3x, f_3x = asd_smooth(asd_3x_raw, f_3x_raw, log_step=8, n_ave=2)
asd_1z, f_1z = asd_smooth(asd_1z_raw, f_1z_raw, log_step=8, n_ave=2)
asd_2z, f_2z = asd_smooth(asd_2z_raw, f_2z_raw, log_step=8, n_ave=2)
asd_3z, f_3z = asd_smooth(asd_3z_raw, f_3z_raw, log_step=8, n_ave=2)

# at each run, change this accordingly to select the desired degree of freedom or the desired HoQI
asd, f = asd_3x, f_3x
asd_raw, f_raw, = asd_3x_raw, f_3x_raw

# finding the peak frequencies including the corresponding prominences
peaks, properties = find_peaks(np.log10(asd_raw[f_raw <= 100]), prominence=3) # it is undesirable for the peak detection to be (potentially) affected by the smoothing

# creating the figure in which the overlapping ASD's will be plotted
figure = plt.figure()

# subsequently, the ASD of the non-fitted data (both the smoothened and the non-smoothened ('raw') one) can be plotted in the following way (note that f_min = 1/segment_time)
plt.loglog(f, asd, color='red', label='non-fitted data')
# plt.loglog(f_raw, asd_raw, color='red', alpha=0.5, label='non-fitted data (raw)')
print("Peak frequencies (Hz) of the non-fitted data:", np.array2string(f_raw[f_raw <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))

# we can do the exact same analysis for the single ellipse fitted data
gwpy = get_asd(x_list_single, fs_set, segment_time_set); asd_x_raw, f_x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(y_list_single, fs_set, segment_time_set); asd_y_raw, f_y_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(z_list_single, fs_set, segment_time_set); asd_z_raw, f_z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rx_list_single, fs_set, segment_time_set); asd_Rx_raw, f_Rx_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Ry_list_single, fs_set, segment_time_set); asd_Ry_raw, f_Ry_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rz_list_single, fs_set, segment_time_set); asd_Rz_raw, f_Rz_raw = gwpy.value, gwpy.frequencies.value

asd_x, f_x = asd_smooth(asd_x_raw, f_x_raw, log_step=8, n_ave=2)
asd_y, f_y = asd_smooth(asd_y_raw, f_y_raw, log_step=8, n_ave=2)
asd_z, f_z = asd_smooth(asd_z_raw, f_z_raw, log_step=8, n_ave=2)
asd_Rx, f_Rx = asd_smooth(asd_Rx_raw, f_Rx_raw, log_step=8, n_ave=2)
asd_Ry, f_Ry = asd_smooth(asd_Ry_raw, f_Ry_raw, log_step=8, n_ave=2)
asd_Rz, f_Rz = asd_smooth(asd_Rz_raw, f_Rz_raw, log_step=8, n_ave=2)

gwpy = get_asd(length_1x_list_single, fs_set, segment_time_set); asd_1x_raw, f_1x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2x_list_single, fs_set, segment_time_set); asd_2x_raw, f_2x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3x_list_single, fs_set, segment_time_set); asd_3x_raw, f_3x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_1z_list_single, fs_set, segment_time_set); asd_1z_raw, f_1z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2z_list_single, fs_set, segment_time_set); asd_2z_raw, f_2z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3z_list_single, fs_set, segment_time_set); asd_3z_raw, f_3z_raw = gwpy.value, gwpy.frequencies.value

asd_1x, f_1x = asd_smooth(asd_1x_raw, f_1x_raw, log_step=8, n_ave=2)
asd_2x, f_2x = asd_smooth(asd_2x_raw, f_2x_raw, log_step=8, n_ave=2)
asd_3x, f_3x = asd_smooth(asd_3x_raw, f_3x_raw, log_step=8, n_ave=2)
asd_1z, f_1z = asd_smooth(asd_1z_raw, f_1z_raw, log_step=8, n_ave=2)
asd_2z, f_2z = asd_smooth(asd_2z_raw, f_2z_raw, log_step=8, n_ave=2)
asd_3z, f_3z = asd_smooth(asd_3z_raw, f_3z_raw, log_step=8, n_ave=2)

# at each run, change this accordingly to select the desired degree of freedom or the desired HoQI
asd, f = asd_3x, f_3x
asd_raw, f_raw, = asd_3x_raw, f_3x_raw

peaks, properties = find_peaks(np.log10(asd_raw[f_raw <= 100]), prominence=3)

plt.loglog(f, asd, color='orange', label='single ellipse fitted data')
# plt.loglog(f_raw, asd_raw, color='orange', alpha=0.5, label='single ellipse fitted data (raw)')
print("Peak frequencies (Hz) of the single ellipse fitted data:", np.array2string(f_raw[f_raw <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))
    
# we can again do the exact same analysis for the windowed ellipse fitted data
gwpy = get_asd(x_list_windowed, fs_set, segment_time_set); asd_x_raw, f_x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(y_list_windowed, fs_set, segment_time_set); asd_y_raw, f_y_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(z_list_windowed, fs_set, segment_time_set); asd_z_raw, f_z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rx_list_windowed, fs_set, segment_time_set); asd_Rx_raw, f_Rx_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Ry_list_windowed, fs_set, segment_time_set); asd_Ry_raw, f_Ry_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rz_list_windowed, fs_set, segment_time_set); asd_Rz_raw, f_Rz_raw = gwpy.value, gwpy.frequencies.value

asd_x, f_x = asd_smooth(asd_x_raw, f_x_raw, log_step=8, n_ave=2)
asd_y, f_y = asd_smooth(asd_y_raw, f_y_raw, log_step=8, n_ave=2)
asd_z, f_z = asd_smooth(asd_z_raw, f_z_raw, log_step=8, n_ave=2)
asd_Rx, f_Rx = asd_smooth(asd_Rx_raw, f_Rx_raw, log_step=8, n_ave=2)
asd_Ry, f_Ry = asd_smooth(asd_Ry_raw, f_Ry_raw, log_step=8, n_ave=2)
asd_Rz, f_Rz = asd_smooth(asd_Rz_raw, f_Rz_raw, log_step=8, n_ave=2)

gwpy = get_asd(length_1x_list_windowed, fs_set, segment_time_set); asd_1x_raw, f_1x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2x_list_windowed, fs_set, segment_time_set); asd_2x_raw, f_2x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3x_list_windowed, fs_set, segment_time_set); asd_3x_raw, f_3x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_1z_list_windowed, fs_set, segment_time_set); asd_1z_raw, f_1z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2z_list_windowed, fs_set, segment_time_set); asd_2z_raw, f_2z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3z_list_windowed, fs_set, segment_time_set); asd_3z_raw, f_3z_raw = gwpy.value, gwpy.frequencies.value

asd_1x, f_1x = asd_smooth(asd_1x_raw, f_1x_raw, log_step=8, n_ave=2)
asd_2x, f_2x = asd_smooth(asd_2x_raw, f_2x_raw, log_step=8, n_ave=2)
asd_3x, f_3x = asd_smooth(asd_3x_raw, f_3x_raw, log_step=8, n_ave=2)
asd_1z, f_1z = asd_smooth(asd_1z_raw, f_1z_raw, log_step=8, n_ave=2)
asd_2z, f_2z = asd_smooth(asd_2z_raw, f_2z_raw, log_step=8, n_ave=2)
asd_3z, f_3z = asd_smooth(asd_3z_raw, f_3z_raw, log_step=8, n_ave=2)

# at each run, change this accordingly to select the desired degree of freedom or the desired HoQI
asd, f = asd_3x, f_3x
asd_raw, f_raw, = asd_3x_raw, f_3x_raw

peaks, properties = find_peaks(np.log10(asd_raw[f_raw <= 100]), prominence=3)

plt.loglog(f, asd, color='green', label='windowed ellipse fitted data')
# plt.loglog(f_raw, asd_raw, color='green', alpha=0.5, label='windowed ellipse fitted data (raw)')
print("Peak frequencies (Hz) of the windowed ellipse fitted data:", np.array2string(f_raw[f_raw <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))

# highlighting (and indicating) the peak frequencies in the created plot, including the corresponding prominence
plt.plot(f_raw[f_raw <= 100][peaks], asd_raw[f_raw <= 100][peaks], "gv")
for i, frequency in enumerate(f_raw[f_raw <= 100][peaks]):
    prominence = properties["prominences"][i]
    y_text = asd_raw[f_raw <= 100][peaks][i]
    
    plt.axvline(x=frequency, color='r', linestyle='--', linewidth=0.8, alpha=0.8)
    plt.text(
        frequency * 1.1,       
        y_text,
        f"f = {frequency:.2f} Hz\nprominence = {prominence:.2f}",
        fontsize=12,
        color='r',
        va='center',
        rotation=0)

# we can do the exact same analysis for the raw data
gwpy = get_asd(x_list_dataset, fs_set, segment_time_set); asd_x_raw, f_x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(y_list_dataset, fs_set, segment_time_set); asd_y_raw, f_y_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(z_list_dataset, fs_set, segment_time_set); asd_z_raw, f_z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rx_list_dataset, fs_set, segment_time_set); asd_Rx_raw, f_Rx_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Ry_list_dataset, fs_set, segment_time_set); asd_Ry_raw, f_Ry_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(Rz_list_dataset, fs_set, segment_time_set); asd_Rz_raw, f_Rz_raw = gwpy.value, gwpy.frequencies.value

asd_x, f_x = asd_smooth(asd_x_raw, f_x_raw, log_step=8, n_ave=2)
asd_y, f_y = asd_smooth(asd_y_raw, f_y_raw, log_step=8, n_ave=2)
asd_z, f_z = asd_smooth(asd_z_raw, f_z_raw, log_step=8, n_ave=2)
asd_Rx, f_Rx = asd_smooth(asd_Rx_raw, f_Rx_raw, log_step=8, n_ave=2)
asd_Ry, f_Ry = asd_smooth(asd_Ry_raw, f_Ry_raw, log_step=8, n_ave=2)
asd_Rz, f_Rz = asd_smooth(asd_Rz_raw, f_Rz_raw, log_step=8, n_ave=2)

gwpy = get_asd(length_1x_list_dataset, fs_set, segment_time_set); asd_1x_raw, f_1x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2x_list_dataset, fs_set, segment_time_set); asd_2x_raw, f_2x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3x_list_dataset, fs_set, segment_time_set); asd_3x_raw, f_3x_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_1z_list_dataset, fs_set, segment_time_set); asd_1z_raw, f_1z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_2z_list_dataset, fs_set, segment_time_set); asd_2z_raw, f_2z_raw = gwpy.value, gwpy.frequencies.value
gwpy = get_asd(length_3z_list_dataset, fs_set, segment_time_set); asd_3z_raw, f_3z_raw = gwpy.value, gwpy.frequencies.value

asd_1x, f_1x = asd_smooth(asd_1x_raw, f_1x_raw, log_step=8, n_ave=2)
asd_2x, f_2x = asd_smooth(asd_2x_raw, f_2x_raw, log_step=8, n_ave=2)
asd_3x, f_3x = asd_smooth(asd_3x_raw, f_3x_raw, log_step=8, n_ave=2)
asd_1z, f_1z = asd_smooth(asd_1z_raw, f_1z_raw, log_step=8, n_ave=2)
asd_2z, f_2z = asd_smooth(asd_2z_raw, f_2z_raw, log_step=8, n_ave=2)
asd_3z, f_3z = asd_smooth(asd_3z_raw, f_3z_raw, log_step=8, n_ave=2)

# at each run, change this accordingly to select the desired degree of freedom or the desired HoQI
asd, f = asd_3x, f_3x
asd_raw, f_raw, = asd_3x_raw, f_3x_raw

peaks, properties = find_peaks(np.log10(asd_raw[f_raw <= 100]), prominence=3)

plt.loglog(f, asd, color='blue', label='pre-analysed data')
# plt.loglog(f_raw, asd_raw, color='blue', alpha=0.5, label='pre-analysed data (raw)')
print("Peak frequencies (Hz) of the pre-analysed data:", np.array2string(f_raw[f_raw <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))

# creating the actual plot with the overlapping ASD's
plt.xlabel("Frequency (Hz)")
if (asd == asd_Rx).all() or (asd == asd_Ry).all() or (asd == asd_Rz).all():
    plt.ylabel("ASD (urad Hz^(-1/2))")
else:
    plt.ylabel("ASD (um Hz^(-1/2))")
plt.xlim(1e-3, 5e2)
plt.ylim(1e-7, 1e3)
plt.grid(True, which="both")
plt.title('Smoothened and non-smoothened ASD diagrams (3x)')
plt.legend(fontsize=12, loc='upper right')
plt.savefig('Overlapping_Aligning_ASDs_Transparent.png', format='png', transparent=True)
plt.show()