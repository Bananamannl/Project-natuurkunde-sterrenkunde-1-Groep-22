import numpy as np
import matplotlib.pyplot as plt

# bepaald snelheid
afstand = np.load ("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
dt = 0.001
snelheid = np.gradient(afstand, dt, axis =0) # berekent de afgeleide 


#----------- PLOT ----------
t = np.arange(afstand.shape[0]) * dt

plt.figure()

# plot alle velocity time diagrams los per HoQI
plt.plot(t,snelheid [:,0], label = 'HoQI 1x')

plt.xlabel('Tijd (s)')
plt.ylabel('Snelheid')
plt.legend()
plt.grid(True)
plt.show()

# plt.plot(t,snelheid [:,1], label = 'HoQI 2x')

# plt.xlabel('Tijd (s)')
# plt.ylabel('Snelheid')
# plt.legend()
# plt.grid(True)
# plt.show()

# plt.plot(t,snelheid [:,2], label = 'HoQI 3x')

# plt.xlabel('Tijd (s)')
# plt.ylabel('Snelheid')
# plt.legend()
# plt.grid(True)
# plt.show()

# plt.plot(t,snelheid [:,3], label = 'HoQI 1z')

# plt.xlabel('Tijd (s)')
# plt.ylabel('Snelheid')
# plt.legend()
# plt.grid(True)
# plt.show()

# plt.plot(t,snelheid [:,4], label = 'HoQI 2z')

# plt.xlabel('Tijd (s)')
# plt.ylabel('Snelheid')
# plt.legend()
# plt.grid(True)
# plt.show()

# plt.plot(t,snelheid [:,5], label = 'HoQI 3z')

# plt.xlabel('Tijd (s)')
# plt.ylabel('Snelheid')
# plt.legend()
# plt.grid(True)
# plt.show()

# plot alle velocity time diagrams van alle HoQI's samen
titels = [          #geeft de goede naam aan het bijbehorende figuur
    "HoQI 1x",
    "HoQI 2x",
    "HoQI 3x",
    "HoQI 1z",
    "HoQI 2z",
    "HoQI 3z"
]

fig, axs = plt.subplots(2, 3, figsize=(12, 8))

for i, ax in enumerate(axs.flat):
    ax.plot(t[::1000], snelheid[::1000, i])
    ax.set_title(titels[i])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Velocity')

plt.tight_layout()
plt.show()