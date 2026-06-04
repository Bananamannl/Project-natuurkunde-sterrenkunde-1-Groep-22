import numpy as np
from gwpy.timeseries import TimeSeries
#zorg dat x de lijst met verplaatsingen wordt:
x = np.array
#trek het gemiddelde eraf om te voorkomen dat je een ziek grote piek rond 0 Hz krijgt
x = x - np.mean(x)

fs = 1000 #Aantal samples per seconde

ts = TimeSeries(x, sample_rate= fs)

ASD = ts.asd(seconds=4) #Maak er een ASD van
#Eventueel nog S