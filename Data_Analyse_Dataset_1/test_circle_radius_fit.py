import numpy as np
from ellipse_fitting_and_reshaping_3_4 import transform
from scipy.optimize import least_squares

Q1, Q2 = np.load("Data_Analyse_Dataset_1\\1xQ1.npy"), np.load("Data_Analyse_Dataset_1\\1xQ2.npy")

def residuals(params, x, y):
    x0, y0, r = params
    return (x - x0) **2 + (y - y0) ** 2 - r ** 2

def circle_fit(x, y):
        results = least_squares(
        residuals,
        x0 = [0, 0, 1],
        args = (x, y)
        )
        x0, y0, r = results.x
        return x0, y0, r
Q1, Q2 = transform(Q1, Q2)

print(circle_fit(Q1, Q2))
