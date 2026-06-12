import numpy as np
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from functions import *

# introductie van belangrijke variabelen
segment_time_set = 1000
fs_set = 1000

# de volgende funcite gebruikt de methode van Welch (met overlap)
def get_asd(data, fs, segment_time):
    """
    Maakt van een lijst met verplaatsingen een 'amplitude spectral density diagram' (ASD-diagram).
    get_asd(datalijst, sample rate, duur van de meting in sec) 
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

# de lijsten met de werkelijke verplaatsingen in alle zes de vrijheidsgraden:
x_lijst, y_lijst, z_lijst, Rx_lijst, Ry_lijst, Rz_lijst  = transformatiematrix(length_1x_lijst, length_2x_lijst, length_3x_lijst, length_1z_lijst, length_2z_lijst, length_3z_lijst)
x_lijst_gefit, y_lijst_gefit, z_lijst_gefit, Rx_lijst_gefit, Ry_lijst_gefit, Rz_lijst_gefit  = transformatiematrix(length_1x_lijst_gefit, length_2x_lijst_gefit, length_3x_lijst_gefit, length_1z_lijst_gefit, length_2z_lijst_gefit, length_3z_lijst_gefit)

# segment time: eventuele uitschieters door ruis worden eruit gemiddeld door de data op te delen in verschillende segmenten, waarna voor elke frequentie de gemiddelde amplitude van al deze segmenten wordt genomen; 1000 betekent dat T_max = 1000 s, dus f_min = 0,001 Hz
# (kies er telkens één)
# asd = get_asd(length_1x_lijst, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_2x_lijst, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_3x_lijst, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_1z_lijst, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_2z_lijst, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
asd = get_asd(length_3z_lijst, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000

# 'smoothen' het diagram door van elke vijf opeenvolgende punten de gemiddelde ASD te nemen:
window = 50
asd_smooth = np.convolve(asd.value, np.ones(window)/window, mode='same')

peaks, properties = find_peaks(np.log10(asd.value[asd.frequencies.value <= 100]), prominence=1.5) # het is onwenselijk dat de piekdetectie beïnvloed wordt door het 'smoothen'

# vervolgens kan de asd (van de zelf afgeleide data) op de volgende manier worden geplot (f_min = 1/segment_time):
plt.figure()
plt.loglog(asd.frequencies.value, asd_smooth)
plt.plot(asd.frequencies.value[asd.frequencies.value <= 100][peaks], asd_smooth[asd.frequencies.value <= 100][peaks], "rv") # de rode markeringen moeten wel netjes op de 'gesmoothede' functie vallen
for i, frequency in enumerate(asd.frequencies.value[asd.frequencies.value <= 100][peaks]):
    prominence = properties["prominences"][i]
    y_val = asd_smooth[asd.frequencies.value <= 100][peaks][i]
    
    plt.axvline(x=frequency, color='r', linestyle='--', linewidth=0.8, alpha=0.8)
    plt.text(
        frequency * 1.1,     
        y_val,
        f"f = {frequency:.2f} Hz\nprominence = {prominence:.2f}",
        fontsize=9,
        color='r',
        va='center',
        rotation=0)
print("Peak frequencies (Hz) of the derivated data:", np.array2string(asd.frequencies.value[peaks], separator=", "))
print("Prominences (strengths of the associated peaks):", np.array2string(properties["prominences"], separator=", "))
plt.xlabel("Frequency (Hz)")
plt.ylabel("ASD (um Hz^(-1/2))") # de eenheid is m Hz^(-1/2), omdat: m is afkomstig van het feit dat we een amplitude meten; per Hz is afkomstig van het feit dat we door de breedte van een segmentje delen om de amplitude onafhankelijk van de segment_time te maken (^(-1/2) komt doordat we van vermogen naar amplitude gaan (vermogen = amplitude^2))
plt.xlim(1e-3, 1e3)
plt.grid(True, which="both")
plt.title('Smoothened ASD diagram for the non-fitted data (HoQI)')
# plt.savefig('ASD_HoQI_non_fitted_data.png')
plt.show()

# ditzelfde kunnen we doen voor de asd van de gefitte data:
# (kies er telkens één)
# asd = get_asd(length_1x_lijst_gefit, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_2x_lijst_gefit, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_3x_lijst_gefit, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_1z_lijst_gefit, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_2z_lijst_gefit, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
asd = get_asd(length_3z_lijst_gefit, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000

# het 'smoothen':
window = 50
asd_smooth = np.convolve(asd.value, np.ones(window)/window, mode='same')

peaks, properties = find_peaks(np.log10(asd.value[asd.frequencies.value <= 100]), prominence=1.5)

# het plotten:
plt.figure()
plt.loglog(asd.frequencies.value, asd_smooth)
plt.plot(asd.frequencies.value[asd.frequencies.value <= 100][peaks], asd_smooth[asd.frequencies.value <= 100][peaks], "rv")
for i, frequency in enumerate(asd.frequencies.value[asd.frequencies.value <= 100][peaks]):
    prominence = properties["prominences"][i]
    y_val = asd_smooth[asd.frequencies.value <= 100][peaks][i]
    
    plt.axvline(x=frequency, color='r', linestyle='--', linewidth=0.8, alpha=0.8)
    plt.text(
        frequency * 1.1,       
        y_val,
        f"f = {frequency:.2f} Hz\nprominence = {prominence:.2f}",
        fontsize=9,
        color='r',
        va='center',
        rotation=0)
print("Peak frequencies (Hz) of the ellipse fitted data:", np.array2string(asd.frequencies.value[peaks], separator=", "))
print("Prominences (strengths of the associated peaks):", np.array2string(properties["prominences"], separator=", "))
plt.xlabel("Frequency (Hz)")
plt.ylabel("ASD (um Hz^(-1/2))") # de eenheid is m Hz^(-1/2), omdat: m is afkomstig van het feit dat we een amplitude meten; per Hz is afkomstig van het feit dat we door de breedte van een segmentje delen om de amplitude onafhankelijk van de segment_time te maken (^(-1/2) komt doordat we van vermogen naar amplitude gaan (vermogen = amplitude^2))
plt.xlim(1e-3, 1e3)
plt.grid(True, which="both")
plt.title('Smoothened ASD diagram for the fitted data (HoQI)')
# plt.savefig('ASD_HoQI_fitted_data')
plt.show()

# zo ook voor de verplaatsingen afkomstig uit de ruwe data:
data_20260421 = Data_Extract('Data_Analysis_Part_1/20260421_HoQIs.txt')

length_1x_dataset = data_20260421["SENS_HOQI_1_H_DISP_LEN"] 
length_2x_dataset = data_20260421["SENS_HOQI_2_H_DISP_LEN"] 
length_3x_dataset = data_20260421["SENS_HOQI_3_H_DISP_LEN"] 
length_1z_dataset = data_20260421["SENS_HOQI_1_V_DISP_LEN"] 
length_2z_dataset = data_20260421["SENS_HOQI_2_V_DISP_LEN"] 
length_3z_dataset = data_20260421["SENS_HOQI_3_V_DISP_LEN"] 

# (kies er telkens één)
# asd = get_asd(length_1x_dataset, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_2x_dataset, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_3x_dataset, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_1z_dataset fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
# asd = get_asd(length_2z_dataset, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000
asd = get_asd(length_3z_dataset, fs=fs_set, segment_time=segment_time_set) # fs is gelijk aan de sample rate, en die ligt in ons experiment vast: 1000 metingen per seconde, dus fs = 1000

# het 'smoothen':
window = 50
asd_smooth = np.convolve(asd.value, np.ones(window)/window, mode='same')

peaks, properties = find_peaks(np.log10(asd.value[asd.frequencies.value <= 100]), prominence=1.5)

# en het plotten:
plt.figure()
plt.loglog(asd.frequencies.value, asd_smooth)
plt.plot(asd.frequencies.value[asd.frequencies.value <= 100][peaks], asd_smooth[asd.frequencies.value <= 100][peaks], "rv")
for i, frequency in enumerate(asd.frequencies.value[asd.frequencies.value <= 100][peaks]):
    prominence = properties["prominences"][i]
    y_val = asd_smooth[asd.frequencies.value <= 100][peaks][i]
    
    plt.axvline(x=frequency, color='r', linestyle='--', linewidth=0.8, alpha=0.8)
    plt.text(
        frequency * 1.1,      
        y_val,
        f"f = {frequency:.2f} Hz\nprominence = {prominence:.2f}",
        fontsize=9,
        color='r',
        va='center',
        rotation=0)
print("Peak frequencies (Hz) of the raw data:", np.array2string(asd.frequencies.value[peaks], separator=", "))
print("Prominences (strengths of the associated peaks):", np.array2string(properties["prominences"], separator=", "))
plt.xlabel("Frequency (Hz)")
plt.ylabel("ASD (um Hz^(-1/2))") # de eenheid is m Hz^(-1/2), omdat: m is afkomstig van het feit dat we een amplitude meten; per Hz is afkomstig van het feit dat we door de breedte van een segmentje delen om de amplitude onafhankelijk van de segment_time te maken (^(-1/2) komt doordat we van vermogen naar amplitude gaan (vermogen = amplitude^2))
plt.xlim(1e-3, 1e3)
plt.grid(True, which="both")
plt.title('Smoothened ASD diagram for the raw data (HoQI)')
# plt.savefig('ASD_HoQI_raw_data.png')
plt.show()