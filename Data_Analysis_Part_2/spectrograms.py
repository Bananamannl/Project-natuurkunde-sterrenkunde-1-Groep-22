import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
import matplotlib.colors as col

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

zesvector_matrix = np.load("Data_Analysis_Part_1/fitted_six_vct_list.npy")
x_lijst_gefit = zesvector_matrix[0:int(3e6), 0]
y_lijst_gefit = zesvector_matrix[0:int(3e6), 1]
z_lijst_gefit = zesvector_matrix[0:int(3e6), 2]
Rx_lijst_gefit = zesvector_matrix[0:int(3e6), 3]
Ry_lijst_gefit = zesvector_matrix[0:int(3e6), 4]
Rz_lijst_gefit = zesvector_matrix[0:int(3e6), 5]

chunk_duration = 10
fs = 1000
chunk_size = chunk_duration * fs

# kies er telkens één:
data = x_lijst_gefit
# data = y_lijst_gefit
# data = z_lijst_gefit
# data = Rx_lijst_gefit
# data = Ry_lijst_gefit
# data = Rz_lijst_gefit

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
if data is x_lijst_gefit or data is y_lijst_gefit or data is z_lijst_gefit:
    plt.colorbar(label='ASD (um Hz$^{-1/2}$)')
else:
    plt.colorbar(label='ASD (urad Hz$^{-1/2}$)')
plt.yscale('log')
plt.xlim(0, 3000)
plt.ylim(1e-3, 5e2)
plt.xlabel('time (s)')
plt.ylabel('freqeuncy (Hz)')
plt.title('Spectrogram (x) - Single Ellipse Fitted Data')
# plt.savefig('Spectrogram_Rz.png')
plt.show()