import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

def Data_Extract(name):
    """
    Data_Extract( str ) -> dictionairy
    This function takes the name (or path) of a raw HoQI data file and extracts the collumns of this file as lists embedded in a dictionairy, using the headers of columns as keys for the lists that are made up of the values of said columns
    """
    with open(name, 'r') as file:
        column_line = file.readline()
        column_names = column_line.split()
        # Removing the # at the start of the column names
        column_names.pop(0)

        dictionairy_columns = {column: [] for column in column_names}
        next(file)

        for line in file:
            line_split = line.split()
            for i in range(0,len(line_split)):
                 dictionairy_columns[column_names[i]].append(float(line_split[i]))
    
    return dictionairy_columns

def bepaling_Q1_Q2(PD1, PD2, PD3):  
    Q1 = np.array(PD1)-np.array(PD2)
    Q2 = np.array(PD1)-np.array(PD3)
    return Q1, Q2

def residuals(params, x, y):
    x0, y0, a, b, theta = params
    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = - (x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    return xp ** 2 / a ** 2 + yp ** 2 / b ** 2 - 1

# totale functie
def transform(x, y, start_parameters=None):
    """
    Takes two np arrays (Q1, Q1) as input. You can also give starting paramaters by adding: start)parameters=[a, b, c, d, e]. Than the function
    fits the data to an ellips and transforms the data to be on the unit circle
    Output is again two np arrays which are the transformed versions of the input arrays
    """
    if start_parameters is None:
        start_parameters = [0, 0, 1, 1, 0]
    results = least_squares(
        residuals,
        x0 = start_parameters,
        args = (x, y)
    )
    x0, y0, a, b, theta = results.x
    vectors = np.column_stack((x, y))
    centre = np.array([x0, y0])
    squeeze = np.array([a, b])
    R = np.array([[np.cos(theta), - np.sin(theta)], 
                  [np.sin(theta), np.cos(theta)]])
    centred = vectors - centre
    rotated = centred @ R 
    unit_vectors = rotated / squeeze
    return unit_vectors[:, 0], unit_vectors[:, 1]