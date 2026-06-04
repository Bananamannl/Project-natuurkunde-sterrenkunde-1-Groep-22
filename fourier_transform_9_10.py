import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from arctan_Q1_Q2_5_6_7 import Q1_Q2_Length
from transformatiematrix_8 import transformatiematrix

def get_asd(data, fs, segment_time):
    """
    Maak van een lijst met displacements een amplitude spectral density grafiek.
    get_asd(datalijst, samplerate, duur van de meting in sec) 
    """
    data = np.asarray(data)
    data = data - np.mean(data) #trek het gemiddelde eraf om te voorkomen dat je een enorm grote piek rond 0 Hz krijgt
    ts = TimeSeries(data, sample_rate=fs)
    ASD = ts.asd(seconds=segment_time)
    return ASD

Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('1xQ1.npy'), np.load('1xQ2.npy'), np.load('2xQ1.npy'), np.load('2xQ2.npy'), np.load('3xQ1.npy'), np.load('3xQ2.npy'), np.load('1zQ1.npy'), np.load('1zQ2.npy'), np.load('2zQ1.npy'), np.load('2zQ2.npy'), np.load('3zQ1.npy'), np.load('3zQ2.npy')

length_1x_lijst = Q1_Q2_Length(Q1_1x, Q2_1x)

length_2x_lijst = Q1_Q2_Length(Q1_2x, Q2_2x)

length_3x_lijst = Q1_Q2_Length(Q1_3x, Q2_3x)

length_1z_lijst = Q1_Q2_Length(Q1_1z, Q2_1z)

length_2z_lijst = Q1_Q2_Length(Q1_2z, Q2_2z)

length_3z_lijst = Q1_Q2_Length(Q1_3z, Q2_3z)

x_lijst, y_lijst, z_lijst, Rx_lijst, Ry_lijst, Rz_lijst  = transformatiematrix(length_1x_lijst, length_2x_lijst, length_3x_lijst, length_1z_lijst, length_2z_lijst, length_3z_lijst)

asd = get_asd(x_lijst, fs=1000, segment_time=10)

# Vervolgens kun je de asd op de volgende manier plotten

plt.figure()
plt.loglog(asd.frequencies.value, asd.value)
plt.xlabel("Frequency [Hz]")
plt.ylabel("ASD [displacement]")
plt.grid(True, which="both")
plt.show()