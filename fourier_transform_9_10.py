import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from arctan_Q1_Q2_5_6_7 import Q1_Q2_Length
from transformatiematrix_8 import transformatiematrix

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

# de volgende data is niet per se nodig voor de rest van de code, maar toch handig om bij de hand te hebben
Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('1xQ1.npy'), np.load('1xQ2.npy'), np.load('2xQ1.npy'), np.load('2xQ2.npy'), np.load('3xQ1.npy'), np.load('3xQ2.npy'), np.load('1zQ1.npy'), np.load('1zQ2.npy'), np.load('2zQ1.npy'), np.load('2zQ2.npy'), np.load('3zQ1.npy'), np.load('3zQ2.npy')

length_1x_lijst = -Q1_Q2_Length(Q1_1x, Q2_1x)

length_2x_lijst = Q1_Q2_Length(Q1_2x, Q2_2x)

length_3x_lijst = Q1_Q2_Length(Q1_3x, Q2_3x)

length_1z_lijst = -Q1_Q2_Length(Q1_1z, Q2_1z)

length_2z_lijst = -Q1_Q2_Length(Q1_2z, Q2_2z)

length_3z_lijst = -Q1_Q2_Length(Q1_3z, Q2_3z)

# de lijsten met de werkelijke verplaatsingen in alle zes de vrijheidsgraden:
x_lijst, y_lijst, z_lijst, Rx_lijst, Ry_lijst, Rz_lijst  = transformatiematrix(length_1x_lijst, length_2x_lijst, length_3x_lijst, length_1z_lijst, length_2z_lijst, length_3z_lijst)

# segment time: eventuele uitschieters door ruis worden eruit gemiddeld door de data op te delen in verschillende segmenten, waarna voor elke frequentie de gemiddelde amplitude van al deze segmenten wordt genomen; 1000 betekent dat T_max = 1000 s, dus f_min = 0,001 Hz
# (kies er telkens één)
asd = get_asd(x_lijst, fs=1000, segment_time=1000) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(y_lijst, fs=1000, segment_time=1000) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(z_lijst, fs=1000, segment_time=1000) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(Rx_lijst, fs=1000, segment_time=1000) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(Ry_lijst, fs=1000, segment_time=1000) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(Rz_lijst, fs=1000, segment_time=1000) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000

# vervolgens kan de asd op de volgende manier worden geplot (f_min = 1/segment_time):

plt.figure()
plt.loglog(asd.frequencies.value, asd.value)
plt.xlabel("Frequency [Hz]")
plt.ylabel("ASD [m Hz^(-1/2)]") # de eenheid is m Hz^(-1/2), omdat: m is afkomstig van het feit dat we een amplitude meten; per Hz is afkomstig van het feit dat we door de breedte van een segmentje delen om de amplitude onafhankelijk van de segment_time te maken (^(-1/2) komt doordat we van vermogen naar amplitude gaan (vermogen = amplitude^2))
plt.xlim(1e-3, 1e-1)
plt.grid(True, which="both")
plt.show()