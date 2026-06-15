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

# the following function makes use of Welch's method (including overlap)
def get_asd(data, fs, segment_time):
    """
    Maakt van een list met verplaatsingen een 'amplitude spectral density diagram' (ASD-diagram).
    get_asd(datalist, sample rate, duur van de meting in sec) 
    """
    data = np.asarray(data)
    data = data - np.mean(data) # trek het gemiddelde af van elk element in de list om een enorm grote piek rond 0 Hz (= geen trilling, een constante waarde) te voorkomen (in andere woorden: centreer de trilling rond om de y-as)
    ts = TimeSeries(data, sample_rate=fs)
    ASD = ts.asd(segment_time, overlap=segment_time/2) # inzake de overlap: de wiskunde achter de code gaat er blindelings vanuit dat segmenten zich herhalen, waardoor de code de data naar 0 'duwt' aan de randen van een segment om eventuele sprongen (heel kleine, niet daadwerkelijk aanwezige frequenties) te voorkomen - de 50/50 overlap zorgt ervoor dat elk datapunt ten minste één keer goed wordt meegenomen
    return ASD

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
# note: we removed the last 150 elements of the 1x, 2x, 1z, 2z, and 3z lists to make those lists the same length as the 3x list, of which the last 150 elements got removed automatically in the standard_step_window_ellipse_fitting function (since window_size_3x = 210 and 3.000.000 mod 210 ≡ 150)
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
# defining the different ASD's for the displacements in all six degrees of freedom
asd_x, f_x = asd_smooth(x_list, 1/fs_set)
asd_y, f_y = asd_smooth(y_list, 1/fs_set)
asd_z, f_z = asd_smooth(z_list, 1/fs_set)
asd_Rx, f_Rz = asd_smooth(Rx_list, 1/fs_set)
asd_Ry, f_Ry = asd_smooth(Ry_list, 1/fs_set)
asd_Rz, f_Rz = asd_smooth(Rz_list, 1/fs_set)

# defining the different ASD's for the direct HoQI displacements
asd_1x, f_1x = asd_smooth(length_1x_list, 1/fs_set)
asd_2x, f_2x = asd_smooth(length_2x_list, 1/fs_set)
asd_3x, f_3x = asd_smooth(length_3x_list, 1/fs_set)
asd_1z, f_1z = asd_smooth(length_1z_list, 1/fs_set)
asd_2z, f_2z = asd_smooth(length_2z_list, 1/fs_set)
asd_3z, f_3z = asd_smooth(length_3z_list, 1/fs_set)

# at each run, change this accordingly to select the desired degree of freedom
asd, f = asd_3x, f_3x

# finding the peak frequencies including the corresponding prominences
peaks, properties = find_peaks(np.log10(asd[f <= 100]), prominence=1.5) # het is onwenselijk dat de piekdetectie beïnvloed wordt door het 'smoothen'

# subsequently, the ASD of the non-fitted data can be plotted in the following way (note that f_min = 1/segment_time):
figure = plt.figure()
plt.loglog(f, asd, color='red', label='non-fitted data')
print("Peak frequencies (Hz) of the non-fitted data:", np.array2string(f[f <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))

# we can do the exact same analysis for the single ellipse fitted data
asd_x, f_x = asd_smooth(x_list_single, 1/fs_set)
asd_y, f_y = asd_smooth(y_list_single, 1/fs_set)
asd_z, f_z = asd_smooth(z_list_single, 1/fs_set)
asd_Rx, f_Rx = asd_smooth(Rx_list_single, 1/fs_set)
asd_Ry, f_Ry = asd_smooth(Ry_list_single, 1/fs_set)
asd_Rz, f_Rz = asd_smooth(Rz_list_single, 1/fs_set)

asd_1x, f_1x = asd_smooth(length_1x_list_single, 1/fs_set)
asd_2x, f_2x = asd_smooth(length_2x_list_single, 1/fs_set)
asd_3x, f_3x = asd_smooth(length_3x_list_single, 1/fs_set)
asd_1z, f_1z = asd_smooth(length_1z_list_single, 1/fs_set)
asd_2z, f_2z = asd_smooth(length_2z_list_single, 1/fs_set)
asd_3z, f_3z = asd_smooth(length_3z_list_single, 1/fs_set)

# at each run, change this accordingly to select the desired degree of freedom
asd, f = asd_3x, f_3x

peaks, properties = find_peaks(np.log10(asd[f <= 100]), prominence=1.5)

plt.loglog(f, asd, color='orange', label='single ellipse fitted data')
print("Peak frequencies (Hz) of the single ellipse fitted data:", np.array2string(f[f <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))
    
# we can again do the exact same analysis for the windowed ellipse fitted data
asd_x, f_x = asd_smooth(x_list_windowed, 1/fs_set)
asd_y, f_y = asd_smooth(y_list_windowed, 1/fs_set)
asd_z, f_z = asd_smooth(z_list_windowed, 1/fs_set)
asd_Rx, f_Rx = asd_smooth(Rx_list_windowed, 1/fs_set)
asd_Ry, f_Ry = asd_smooth(Ry_list_windowed, 1/fs_set)
asd_Rz, f_Rz = asd_smooth(Rz_list_windowed, 1/fs_set)

asd_1x, f_1x = asd_smooth(length_1x_list_windowed, 1/fs_set)
asd_2x, f_2x = asd_smooth(length_2x_list_windowed, 1/fs_set)
asd_3x, f_3x = asd_smooth(length_3x_list_windowed, 1/fs_set)
asd_1z, f_1z = asd_smooth(length_1z_list_windowed, 1/fs_set)
asd_2z, f_2z = asd_smooth(length_2z_list_windowed, 1/fs_set)
asd_3z, f_3z = asd_smooth(length_3z_list_windowed, 1/fs_set)

# at each run, change this accordingly to select the desired degree of freedom
asd, f = asd_3x, f_3x

peaks, properties = find_peaks(np.log10(asd[f <= 100]), prominence=1.5)

plt.loglog(f, asd, color='green', label='windowed ellipse fitted data')
print("Peak frequencies (Hz) of the windowed ellipse fitted data:", np.array2string(f[f <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))

# highlighting (and indicating) the peak frequencies in the created plot
plt.plot(f[f <= 100][peaks], asd[f <= 100][peaks], "gv")
for i, frequency in enumerate(f[f <= 100][peaks]):
    prominence = properties["prominences"][i]
    y_text = asd[f <= 100][peaks][i]
    
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
asd_x, f_x = asd_smooth(x_list_dataset, 1/fs_set)
asd_y, f_y = asd_smooth(y_list_dataset, 1/fs_set)
asd_z, f_z = asd_smooth(z_list_dataset, 1/fs_set)
asd_Rx, f_Rx = asd_smooth(Rx_list_dataset, 1/fs_set)
asd_Ry, f_Ry = asd_smooth(Ry_list_dataset, 1/fs_set)
asd_Rz, f_Rz = asd_smooth(Rz_list_dataset, 1/fs_set)

asd_1x, f_1x = asd_smooth(length_1x_list_dataset, 1/fs_set)
asd_2x, f_2x = asd_smooth(length_2x_list_dataset, 1/fs_set)
asd_3x, f_3x = asd_smooth(length_3x_list_dataset, 1/fs_set)
asd_1z, f_1z = asd_smooth(length_1z_list_dataset, 1/fs_set)
asd_2z, f_2z = asd_smooth(length_2z_list_dataset, 1/fs_set)
asd_3z, f_3z = asd_smooth(length_3z_list_dataset, 1/fs_set)

# at each run, change this accordingly to select the desired degree of freedom
asd, f = asd_3x, f_3x

peaks, properties = find_peaks(np.log10(asd[f <= 100]), prominence=1.5)

plt.loglog(f, asd, color='blue', label='pre-analysed data')
print("Peak frequencies (Hz) of the pre-analysed data:", np.array2string(f[f <= 100][peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))

# creating the actual plot with the overlapping ASD's
plt.xlabel("Frequency (Hz)")
if (asd == asd_smooth(Rx_list_dataset, 1/fs_set)[0]).all() or \
   (asd == asd_smooth(Ry_list_dataset, 1/fs_set)[0]).all() or \
   (asd == asd_smooth(Rz_list_dataset, 1/fs_set)[0]).all():
    plt.ylabel("ASD (urad Hz^(-1/2))")
else:
    plt.ylabel("ASD (um Hz^(-1/2))")
plt.xlim(1e-3, 1e3)
plt.ylim(1e-7, 1e2)
plt.grid(True, which="both")
plt.title('Smoothened ASD diagrams (3x)')
plt.legend(fontsize=12, loc='upper right')
plt.savefig('Overlapping_ASDs.png')
plt.show()