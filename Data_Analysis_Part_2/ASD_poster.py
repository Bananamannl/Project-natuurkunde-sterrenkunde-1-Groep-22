import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries
from scipy.signal import find_peaks

# Omdat deze functies in jouw omgeving staan, importeren we ze hier:
from functions import *
from frequency_dependent_smoothing import *

# =========================
# Instellingen & Parameters
# =========================
segment_time_set = 1000
fs_set = 1000

# Index 2 komt overeen met HoQI 3x (volgorde: 1x, 2x, 3x, 1z, 2z, 3z)
hoqi_index = 2 

# =========================
# Load saved data van Script 1
# =========================
raw_HoQI_disp       = np.load('Endproduct_code/raw_HoQI_displacement_data.npy', allow_pickle=True)[hoqi_index]
single_ellipse_disp = np.load('Endproduct_code/single_ellipse_HoQI_displacement_data.npy', allow_pickle=True)[hoqi_index]
windowed_ellipse_disp = np.load('Endproduct_code/windowed_ellipse_HoQI_displacement_data.npy', allow_pickle=True)[hoqi_index]

# =========================
# ASD Berekeningen & Smoothing
# =========================
# 1. Non-fitted
gwpy_raw = get_asd(raw_HoQI_disp, fs_set, segment_time_set)
asd_raw_raw, f_raw = gwpy_raw.value, gwpy_raw.frequencies.value
asd_raw, f_raw = asd_smooth(asd_raw_raw, f_raw, log_step=8, n_ave=2)

# 2. Single Ellipse Fitted
gwpy_single = get_asd(single_ellipse_disp, fs_set, segment_time_set)
asd_single_raw, f_single = gwpy_single.value, gwpy_single.frequencies.value
asd_single, f_single = asd_smooth(asd_single_raw, f_single, log_step=8, n_ave=2)

# 3. Windowed Ellipse Fitted
gwpy_windowed = get_asd(windowed_ellipse_disp, fs_set, segment_time_set)
asd_windowed_raw, f_windowed = gwpy_windowed.value, gwpy_windowed.frequencies.value
asd_windowed, f_windowed = asd_smooth(asd_windowed_raw, f_windowed, log_step=8, n_ave=2)

# =========================
# Peak detection op de windowed data
# =========================
mask = f_windowed <= 100
asd_windowed_filtered = asd_windowed[mask]
f_windowed_filtered = f_windowed[mask]

# Peak detection uitgevoerd op de windowed data met een prominence van 1.5
peaks, properties = find_peaks(np.log10(asd_windowed_filtered), prominence=1.5)

# Terminal outputs voor controle
print("Peak frequencies (Hz) of the windowed ellipse fitted data:", np.array2string(f_windowed_filtered[peaks], separator=", "))
print("Prominences:", np.array2string(properties["prominences"], separator=", "))

# =========================
# Plot instellingen (Exacte Style Match)
# =========================
# Foutloze methode om mathtext (zoals exponenten) exact het reguliere lettertype te laten overnemen
plt.rcParams['mathtext.default'] = 'regular'

fig, ax = plt.subplots(figsize=(12, 8))

# Transparante achtergronden
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

# De drie ASD lijnen log-log plotten
ax.loglog(f_raw, asd_raw, color='red', linewidth=1.5, label='Non-fitted data')
ax.loglog(f_single, asd_single, color='deepskyblue', linewidth=1.5, label='Single ellipse fitted data')
ax.loglog(f_windowed, asd_windowed, color='limegreen', linewidth=1.5, label='Windowed ellipse fitted data')

# Hoogtepunten van de pieken toevoegen (Groen: "gv")
f_peaks_100 = f_windowed_filtered[peaks]
asd_peaks_100 = asd_windowed_filtered[peaks]
ax.plot(f_peaks_100, asd_peaks_100, "gv", markersize=8)

# Verticale hulplijnen en tekstlabels voor de gedetecteerde pieken (Limegreen)
for i, frequency in enumerate(f_peaks_100):
    prominence = properties["prominences"][i]
    y_text = asd_peaks_100[i]
    
    ax.axvline(x=frequency, color='limegreen', linestyle='--', linewidth=1.0, alpha=0.6)
    ax.text(
        frequency * 1.15,        
        y_text * 1.15,
        f"f ≈ {frequency:.2f} Hz\nprominence ≈ {prominence:.2f}",
        fontsize=13.5,       
        color='limegreen',
        va='center',
        rotation=0
    )

# Assen opmaken (Wit, groot en dik)
ax.set_xlabel("Frequency (Hz)", color="white", fontsize=20, labelpad=10)

# Echte exponent via mathtext, maar dankzij 'regular' in 100% hetzelfde lettertype als de rest
ax.set_ylabel(r"Displacement ASD (µm Hz$^{-1/2}$)", color="white", fontsize=20, labelpad=10)
ax.set_title("Smoothened ASD diagram for HoQI displacements (3x)", color="white", fontsize=31, fontweight="bold", pad=20, loc='center')
ax.tick_params(axis="both", colors="white", labelsize=14, width=2, length=6, which='both')

# Grenzen instellen conform jouw wens
ax.set_xlim(1e-3, 5e2)
ax.set_ylim(1e-7, 1e3)

# Spines (witte, dikke randen)
for spine in ax.spines.values():
    spine.set_color("white")
    spine.set_linewidth(2.5)

# Grid instellen (Doorgetrokken lijnen "-" met licht aangepaste alpha voor balans)
ax.grid(color="white", alpha=0.25, which="both", linestyle="-")

# Legenda stylen (fontsize=14, Transparante box, witte letters)
legend = ax.legend(fontsize=14, loc='upper right', framealpha=0.1)
for text in legend.get_texts():
    text.set_color("white")

plt.tight_layout()

# Opslaan als transparante high-res PNG
plt.savefig(
    'Endproduct_code/ASD_plot_HoQI_displacements.png',
    dpi=300,
    bbox_inches="tight",
    transparent=True
)

plt.show()