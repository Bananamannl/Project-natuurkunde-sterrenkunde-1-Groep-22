import numpy as np
from scipy.optimize import least_squares

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

    opt_phase_wrap = np.arctan(Q1, Q2)

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

import numpy as np
from gwpy.timeseries import TimeSeries

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

def transformatiematrix (ax, bx, cx, az, bz, cz):
    R = 0.815

    x = (1/3) * (-2 * ax + bx + cx)
    y = (1/np.sqrt(3)) * (-bx + cx)
    z = (1/3) * (az + bz + cz)
    Rx = (1/(3*R)) * (2 * az - bz - cz)
    Ry = (1/(np.sqrt(3) * R)) * (bz - cz)
    Rz = (1/(3*R)) * (ax + bx + cx)

    return x, y, z, Rx, Ry, Rz

def parameters(x, y, start_parameters=None):
    """
    Takes Q1 and Q2 data (np.array's) and spits out the fitting parameters
    the output is in the form of a 6-dim vector:
    (x0, y0, theta, a, b, area)
    """
    if start_parameters is None:
        start_parameters = [0, 0, 1, 1, 0]
    results = least_squares(
        residuals,
        x0 = start_parameters,
        args = (x, y)
    )
    x0, y0, a, b, theta = results.x
    if b > a:
        a, b = b, a
        theta += np.pi / 2
    area = np.pi * a * b
    vector = np.column_stack((x0, y0, theta, a, b, area))
    start_parameters = [x0, y0, a, b, theta]
    return vector, start_parameters

def parameters_timeseries(x, y, window_size=None, step_size=None):
    if window_size is None:
        window_size = 1000
    if step_size is None:
        step_size = 100

    vectoren = []
    fit_parameters = [0, 0, 1, 1, 0]

    for start in range(0, len(x) - window_size + 1, step_size):
        end = start + window_size

        part_Q1 = x[start:end]
        part_Q2 = y[start:end]
        
        vector, fit_parameters = parameters(part_Q1, part_Q2, start_parameters= fit_parameters)
        vectoren.append(np.ravel(vector))
    return np.array(vectoren)

def standard_step_window_ellipse_fitting(Q1, Q2, window_size):

    # This outputs a 6 x floor(len(Q1) / window_size) matrix with the parameters of the differen ellipses. The bottom row is area, which we don't need, so we remove it
    params_matrix = parameters_timeseries(Q1,Q2, window_size=window_size, step_size=window_size)[ : , 0:5]

    return_Q1 = []
    return_Q2 = []
    for start in range(0, len(Q1) - window_size + 1, window_size):
        end = start + window_size

        part_Q1 = Q1[start:end]
        part_Q2 = Q2[start:end]
        
        x0, y0, a, b, theta = params_matrix[int(start / window_size), : ]
        vectors = np.column_stack((part_Q1, part_Q2))
        centre = np.array([x0, y0])
        squeeze = np.array([a, b])
        R = np.array([[np.cos(theta), - np.sin(theta)], 
                    [np.sin(theta), np.cos(theta)]])
        centred = vectors - centre
        rotated = centred @ R
        unit_vectors = rotated / squeeze
        transformed_part_Q1, transformed_part_Q2 = unit_vectors[:, 0], unit_vectors[:, 1]
        return_Q1.append(list(transformed_part_Q1))
        return_Q2.append(list(transformed_part_Q2))

    return np.array(return_Q1).flatten(), np.array(return_Q2).flatten()

# Defining function with overlap
def variable_step_window_ellipse_fitting(Q1, Q2, window_size, step_size):
    # This outputs a 6 x floor(len(Q1) / window_size) matrix with the parameters of the differen ellipses. The bottom row is area, which we don't need, so we remove it
    params_matrix = parameters_timeseries(Q1,Q2, window_size=window_size, step_size=step_size)[ : , 0:5]

    return_Q1 = []
    return_Q2 = []
    for start in range(window_size-step_size, len(Q1) - window_size + 1, step_size):
        end = start + step_size

        part_Q1 = Q1[start:end]
        part_Q2 = Q2[start:end]
        
        list_x0, list_y0, list_a, list_b, list_theta = np.transpose(params_matrix[int((start / step_size) - (window_size / step_size) + 1) : int((start / step_size) + (window_size / step_size)), : ])
        vectors = np.column_stack((part_Q1, part_Q2))

        x0 = np.average(list_x0)
        y0 = np.average(list_y0)
        a = np.average(list_a)
        b = np.average(list_b)
        theta = np.average(list_theta)

        centre = np.array([x0, y0])
        squeeze = np.array([a, b])
        R = np.array([[np.cos(theta), - np.sin(theta)], 
                    [np.sin(theta), np.cos(theta)]])
        centred = vectors - centre
        rotated = centred @ R
        unit_vectors = rotated / squeeze
        transformed_part_Q1, transformed_part_Q2 = unit_vectors[:, 0], unit_vectors[:, 1]
        return_Q1.append(list(transformed_part_Q1))
        return_Q2.append(list(transformed_part_Q2))

    return np.array(return_Q1).flatten(), np.array(return_Q2).flatten()