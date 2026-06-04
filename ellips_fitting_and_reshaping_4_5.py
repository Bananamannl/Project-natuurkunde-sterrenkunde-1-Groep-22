import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt


#Zorg dat Q1 en Q2 numpy arrays zijn
#eerst het de modelfunctie definieren
def residuals(params, x, y):
    x0, y0, a, b, theta = params
    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = (x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    return xp ** 2 / a ** 2 + yp ** 2 / b ** 2 - 1

results = least_squares(
    residuals, #we fitten de modelfunctie
    x0 = [0, 0, 1, 1, 0], #dit zijn de startcondities voor de fit
    args = (Q1, Q2) #Dit wordt dus de data die gefit wordt
)

x0, y0, a, b, theta = results.x

#Maak een vector van Q1 en Q2:
vectors = np.column_stack((Q1, Q2))
centre = np.array([x0, y0])
squeeze = np.array([a, b])
R = np.array([[np.cos(theta), - np.sin(theta)], 
              [np.sin(theta), np.cos(theta)]]).T
M = squeeze @ R
#Nu moeten we Q1 en Q2 terug transformeren naar de eenheidscirkel:
# Verplaatsen naar oorsprong
centred = vectors - centre
rotated = centred @ R 
unit_vectors = rotated / squeeze
#Test door te plotten:

plt.figure()
plt.scatter(vectors[:, 0, vectors[:, 1]], s=3)
plt.scatter(unit_vectors[:, 0], unit_vectors[:, 1], s=5)
plt.axis("equal")
plt.grid()
plt.show()

#####################
#Totale functie
def transform(Q1, Q2):
    """
    Takes two np arrays (Q1, Q1) as input, fits it to an ellips and transforms the data to be on the unit circle
    Output is again two np arrays which are the transformed versions of the input arrays
    """
    results = least_squares(
        residuals,
        x0 = [0, 0, 1, 1, 0],
        args = (Q1, Q2)
    )
    x0, y0, a, b, theta = results.x
    vectors = np.column_stack((Q1, Q2))
    centre = np.array([x0, y0])
    squeeze = np.array([a, b])
    R = np.array([[np.cos(theta), - np.sin(theta)], 
                  [np.sin(theta), np.cos(theta)]]).T
    centred = vectors - centre
    rotated = centred @ R 
    unit_vectors = rotated / squeeze
    return unit_vectors[:, 0], unit_vectors[:, 1]
Q1_new, Q2_new = transform(Q1, Q2)

plt.figure()
plt.scatter(Q1, Q2, s=3)
plt.scatter(Q1_new, Q2_new, s=5)
plt.axis("equal")
plt.grid()
plt.show()
#%%
import numpy as np
from data_extraction_1 import *
from bepaling_Q1_Q2_2 import *
HoQI_data = Data_Extract('20260421_HoQIs.txt') 

# First HoQI PD1, PD2, PD3: 
# SENS_HOQI_1_H_INP_SIN_IN SENS_HOQI_1_H_INP_COS_IN SENS_HOQI_1_H_INP_MCOS_IN
HoQI_1_Q1, HoQI_1_Q2 = bepaling_Q1_Q2(HoQI_data['SENS_HOQI_1_H_INP_SIN_IN'], HoQI_data['SENS_HOQI_1_H_INP_COS_IN'], HoQI_data['SENS_HOQI_1_H_INP_MCOS_IN'])
print(HoQI_1_Q1, HoQI_1_Q2)
Q1, Q2 = transform(HoQI_1_Q1, HoQI_1_Q2)
