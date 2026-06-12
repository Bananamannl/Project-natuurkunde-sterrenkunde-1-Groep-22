import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
import matplotlib.colors as col

from functions import *

# de volgende funcite gebruikt de methode van Welch (met overlap)
def get_asd(data, fs, segment_time):
    """
    Maak van een lijst met displacements een amplitude spectral density grafiek.
    get_asd(datalijst, samplerate, duur van de meting in sec) 
    """
    data = np.asarray(data)
    data = data - np.mean(data) # trek het gemiddelde af van elk element in de lijst om een enorm grote piek rond 0 Hz (= geen trilling, een constante waarde) te voorkomen (in andere woorden: centreer de trilling rond om de y-as)
    ts = TimeSeries(data, sample_rate=fs)
    ASD = ts.asd(segment_time, overlap=segment_time/2) # inzake de overlap: de wiskunde achter de code gaat er blindelings vanuit dat segmenten zich herhalen, waardoor de code de data naar 0 'duwt' aan de randen van een segment om eventuele sprongen (heel kleine, niet daadwerkelijk aanwezige frequenties) te voorkomen - de 50/50 overlap zorgt ervoor dat elk datapunt ten minste één keer goed wordt meegenomen
    return ASD

# extracting the Q lists from the saved data files to prevent Python from having to read all the raw data first
Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy'), np.load('Data_Analysis_Part_1/2xQ1.npy'), np.load('Data_Analysis_Part_1/2xQ2.npy'), np.load('Data_Analysis_Part_1/3xQ1.npy'), np.load('Data_Analysis_Part_1/3xQ2.npy'), np.load('Data_Analysis_Part_1/1zQ1.npy'), np.load('Data_Analysis_Part_1/1zQ2.npy'), np.load('Data_Analysis_Part_1/2zQ1.npy'), np.load('Data_Analysis_Part_1/2zQ2.npy'), np.load('Data_Analysis_Part_1/3zQ1.npy'), np.load('Data_Analysis_Part_1/3zQ2.npy')

# the same for the ellips fitted Q lists:
Q1_1x_gefit, Q2_1x_gefit = transform(Q1_1x, Q2_1x)
Q1_2x_gefit, Q2_2x_gefit = transform(Q1_2x, Q2_2x)
Q1_3x_gefit, Q2_3x_gefit = transform(Q1_3x, Q2_3x)
Q1_1z_gefit, Q2_1z_gefit = transform(Q1_1z, Q2_1z)
Q1_2z_gefit, Q2_2z_gefit = transform(Q1_2z, Q2_2z)
Q1_3z_gefit, Q2_3z_gefit = transform(Q1_3z, Q2_3z)

# note: some of these lists contain minus signs due to the polarization plate being turned in the oppositie direction in the original experiment
length_1x_lijst = -Q1_Q2_Length(Q1_1x, Q2_1x)

length_2x_lijst = Q1_Q2_Length(Q1_2x, Q2_2x)

length_3x_lijst = Q1_Q2_Length(Q1_3x, Q2_3x)

length_1z_lijst = -Q1_Q2_Length(Q1_1z, Q2_1z)

length_2z_lijst = -Q1_Q2_Length(Q1_2z, Q2_2z)

length_3z_lijst = -Q1_Q2_Length(Q1_3z, Q2_3z)

# and by using the fitted Q lists:
length_1x_lijst_gefit = -Q1_Q2_Length(Q1_1x_gefit, Q2_1x_gefit)

length_2x_lijst_gefit = Q1_Q2_Length(Q1_2x_gefit, Q2_2x_gefit)

length_3x_lijst_gefit = Q1_Q2_Length(Q1_3x_gefit, Q2_3x_gefit)

length_1z_lijst_gefit = -Q1_Q2_Length(Q1_1z_gefit, Q2_1z_gefit)

length_2z_lijst_gefit = -Q1_Q2_Length(Q1_2z_gefit, Q2_2z_gefit)

length_3z_lijst_gefit = -Q1_Q2_Length(Q1_3z_gefit, Q2_3z_gefit)

chunk_duration = 10
fs = 1000
chunk_size = chunk_duration * fs

# kies er telkens één:
# data = length_1x_lijst_gefit
# data = length_2x_lijst_gefit
# data = length_3x_lijst_gefit
data = length_1z_lijst_gefit
# data = length_2z_lijst_gefit
# data = length_3z_lijst_gefit

asds = []
times = []

for i in range(0, len(data) - chunk_size + 1, chunk_size):
    chunk = data[i : (i + chunk_size)]
    asd_chunk = get_asd(chunk, fs=fs, segment_time=chunk_duration/2)
    asds.append(asd_chunk.value)
    times.append(i / fs) 

frequencies = asd_chunk.frequencies.value
asd_matrix = np.array(asds)  

plt.pcolormesh(
    times, frequencies, asd_matrix.T,
    norm=col.LogNorm(vmin=asd_matrix.min(), vmax=asd_matrix.max()),
    cmap='plasma',
    shading='auto',
    linewidth=0)
plt.colorbar(label='ASD (um Hz$^{-1/2}$)')
plt.yscale('log')
plt.xlim(0, 3000)
plt.ylim(1e-3, 5e2)
plt.xlabel('time (s)')
plt.ylabel('freqeuncy (Hz)')
plt.title('Spectrogram (HoQI) - Fitted Data')
# plt.savefig('Spectrogram_HoQI.png')
plt.show()