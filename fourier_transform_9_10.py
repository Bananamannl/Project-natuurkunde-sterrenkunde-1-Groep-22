import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from data_extraction_1 import *
from transformatiematrix_8 import displacement_dof

x_lijst, y_lijst, z_lijst, Rx_lijst, Ry_lijst, Rz_lijst = displacement_dof

def get_asd(data, fs, segment_time):
    """
    Maak van een lijst met displacements een amplitude spectral density grafiek.
    get_asd(datalijst, samplerate, duur van de meting in sec) 
    """
    data = np.asarray(data)
    data = data - np.mean(data) #trek het gemiddelde eraf om te voorkomen dat je een ziek grote piek rond 0 Hz krijgt
    ts = TimeSeries(data, sample_rate=fs)
    ASD = ts.asd(seconds=segment_time)
    return ASD

# Vervolgens kun je de asd op de volgende manier plotten
# Bijvoorbeeld voor de x-lijst:
asd = get_asd(x_lijst, fs=1000, segment_time=10)

plt.figure()
plt.loglog(asd.frequencies.value, asd.value)
plt.xlabel("Frequency [Hz]")
plt.ylabel("ASD [displacement]")
plt.grid(True, which="both")
plt.show()