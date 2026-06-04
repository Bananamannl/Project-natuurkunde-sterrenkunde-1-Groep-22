import numpy as np
from scipy.optimize import least_squares
#eerst het de modelfunctie definieren
def residuals(params, x, y):
    x0, y0, a, b, theta = params
    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = (x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    return xp ** 2 / a ** 2 + yp ** 2 / b ** 2 - 1

results = least_squares(
    residuals, #we fitten de modelfunctie
    x0 = [0, 0, 1, 1, 0] #dit zijn de startcondities voor de fit
    args = (Q1, Q2) #Dit wordt dus de data die gefit wordt
    #Merk op dat Q1 en Q2 hier de lijst met datapunten is
)

x0, y0, a, b, theta = results.x

#Nu moeten we Q1 en Q2 terug transformeren naar de eenheidscirkel:
c = #dit wordt de vector waarmee de oorsprong is verplaatst
T = #dit wordt de combinatie van de diagonaalmatrix die de x en y-as squeezed en de rotatiematrix R(theta)
#dan krijgen de de volgende transformatie:


