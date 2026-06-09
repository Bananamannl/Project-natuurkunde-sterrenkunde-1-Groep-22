import numpy as np
from scipy.optimize import least_squares
import matplotlib as mt

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

# functie die optical phase en norm terug geeft
def Q1_Q2_Length_opt_phase_norm_Q(Q1, Q2):
    """
    Q1_Q2_Length( np.array, np.array ) - > np.array
    This function takes two lists of Q1 and Q2 made from the HoQI data, and calculates the optical phase. It then uses the optical phase to calculate the measured length at each timestep. This is then outputed as another np.array.
    """
    # The wavelength of the HoQI laser is 1064 nm, adjusted to e-3 to have the outputed length be in um instead
    w_length = 1064e-3 

    opt_phase = np.unwrap(np.arctan2(Q1, Q2))

    length = (opt_phase * w_length)/(4*np.pi)

    Q_absoluut = np.sqrt((Q1)**2 + (Q2)**2)

    return length, opt_phase, Q_absoluut

def Q1_Q2_Opt_Fase(Q1, Q2):
    """
    Q1_Q2_Length( np.array, np.array ) - > np.array
    This function takes two lists of Q1 and Q2 made from the HoQI data, and calculates the optical phase. It then uses the optical phase to calculate the measured length at each timestep. This is then outputed as another np.array.
    """
    # The wavelength of the HoQI laser is 1064 nm, adjusted to e-3 to have the outputed length be in um instead
    w_length = 1064e-3 

    opt_phase = np.unwrap(np.arctan2(Q1, Q2))

    return opt_phase


# note that this function uses lists as input arguments
def Q1_Q2_Length(Q1, Q2):
    """
    Q1_Q2_Length( np.array, np.array ) - > np.array
    This function takes two lists of Q1 and Q2 made from the HoQI data, and calculates the optical phase. It then uses the optical phase to calculate the measured length at each timestep. This is then outputed as another np.array.
    """
    # The wavelength of the HoQI laser is 1064 nm, adjusted to e-3 to have the outputed length be in um instead
    w_length = 1064e-3 

    opt_phase = np.unwrap(np.arctan2(Q1, Q2))

    length = (opt_phase * w_length)/(4*np.pi)

    return length

import numpy as np
from scipy.optimize import least_squares

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