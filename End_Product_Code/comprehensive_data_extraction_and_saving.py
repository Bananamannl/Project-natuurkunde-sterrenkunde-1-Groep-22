"""This code will take a HoQI data file as input, and generate a large selection of .npy quick access data files containing said data processed in all relevant ways."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

## User Input: This will allow the user to select which outputs they want the program to have, and specifically select between different types of outputs (This might eventually be replaced with an actual GUI if I have time)
valid_input = True
print("You can decide what types of data the program outputs into .npy files with the inputs below, afterwards it will run and output the ones you've selected into .npy quickaccess files. Please only answer with y for yes and n for no.")
while valid_input == True:
    all_data = input("Do you want to just have the program output all types of processed data? Input y for yes and n for no besides here: ").lower()
    if all_data == "y" or all_data == "n": 
        valid_input = False
    else:
        print("Wrong input, please only input y for yes or n for no")

choices_dict = {"Q1_Q2_data": True, "raw_data": True, "single_ellipse_data": True, "window_ellipse_data": True, "ellipse_params_timeseries": True,}
if all_data == "n":
    valid_input = True
    while valid_input == True:
        input_var = input("Do you want the program to output the Q1 and Q2 data for all the HoQI's as .npy files? Input y for yes and n for no besides here: ").lower()
        if input_var == "y" or input_var == "n": 
            valid_input = False
        else:
            print("Wrong input, please only input y for yes or n for no")
    if input_var == "n": choices_dict["Q1_Q2_data"] = False

    valid_input = True
    while valid_input == True:
        input_var = input("Do you want the program to output the raw data as .npy files? Input y for yes and n for no besides here: ").lower()
        if input_var == "y" or input_var == "n": 
            valid_input = False
        else:
            print("Wrong input, please only input y for yes or n for no")
    if input_var == "n": choices_dict["raw_data"] = False

    valid_input = True
    while valid_input == True:
        input_var = input("Do you want the program to output the single ellipse fitted data as .npy files? Input y for yes and n for no besides here: ").lower()
        if input_var == "y" or input_var == "n": 
            valid_input = False
        else:
            print("Wrong input, please only input y for yes or n for no")
    if input_var == "n": choices_dict["single_ellipse_data"] = False

    valid_input = True
    while valid_input == True:
        input_var = input("Do you want the program to output the windowed ellipse fitted data as .npy files? Input y for yes and n for no besides here: ").lower()
        if input_var == "y" or input_var == "n": 
            valid_input = False
        else:
            print("Wrong input, please only input y for yes or n for no")
    if input_var == "n": choices_dict["window_ellipse_data"] = False

    valid_input = True
    while valid_input == True:
        input_var = input("Do you want the program to output the ellipse parameters timeseries as .npy files? Input y for yes and n for no besides here: ").lower()
        if input_var == "y" or input_var == "n": 
            valid_input = False
        else:
            print("Wrong input, please only input y for yes or n for no")
    if input_var == "n": choices_dict["ellipse_params_timeseries"] = False

## Extracting the data from the raw data file and adding it to the HoQI_data dictionary 
name = input("Please copy and paste the relative file path to the data file into this input line: ")
with open(name, 'r') as file:
        column_line = file.readline()
        column_names = column_line.split()
        # Removing the # at the start of the column names
        column_names.pop(0)

        HoQI_data = {column: [] for column in column_names}
        next(file)

        for line in file:
            line_split = line.split()
            for i in range(0,len(line_split)):
                 HoQI_data[column_names[i]].append(float(line_split[i]))

## Extracting Q1 and Q2 from the PD1, PD2 and PD3 data and saving them as .npy lists
PD1_1x = HoQI_data["SENS_HOQI_1_H_INP_SIN_IN"] 
PD2_1x = HoQI_data["SENS_HOQI_1_H_INP_COS_IN"]
PD3_1x = HoQI_data["SENS_HOQI_1_H_INP_MCOS_IN"]
PD1_2x = HoQI_data["SENS_HOQI_2_H_INP_SIN_IN"]
PD2_2x = HoQI_data["SENS_HOQI_2_H_INP_COS_IN"]
PD3_2x = HoQI_data["SENS_HOQI_2_H_INP_MCOS_IN"]
PD1_3x = HoQI_data["SENS_HOQI_3_H_INP_SIN_IN"]
PD2_3x = HoQI_data["SENS_HOQI_3_H_INP_COS_IN"]
PD3_3x = HoQI_data["SENS_HOQI_3_H_INP_MCOS_IN"]
PD1_1z = HoQI_data["SENS_HOQI_1_V_INP_SIN_IN"]
PD2_1z = HoQI_data["SENS_HOQI_1_V_INP_COS_IN"]
PD3_1z = HoQI_data["SENS_HOQI_1_V_INP_MCOS_IN"]
PD1_2z = HoQI_data["SENS_HOQI_2_V_INP_SIN_IN"]
PD2_2z = HoQI_data["SENS_HOQI_2_V_INP_COS_IN"]
PD3_2z = HoQI_data["SENS_HOQI_2_V_INP_MCOS_IN"]
PD1_3z = HoQI_data["SENS_HOQI_3_V_INP_SIN_IN"]
PD2_3z = HoQI_data["SENS_HOQI_3_V_INP_COS_IN"]
PD3_3z = HoQI_data["SENS_HOQI_3_V_INP_MCOS_IN"]

def determination_Q1_Q2(PD1, PD2, PD3):
    """
    determination_Q1_Q2(list, list, list) -> np.aray, np.array
    This function takes a PD1, PD2 and PD3 from a specific HoQI and calculates the Q1 and Q2 lists for said HoQI using the formula provided in Cooper 2018.
    """  
    Q1 = np.array(PD1)-np.array(PD2)
    Q2 = np.array(PD1)-np.array(PD3)
    return Q1, Q2

Q1_1x, Q2_1x = determination_Q1_Q2(PD1_1x, PD2_1x, PD3_1x)
Q1_2x, Q2_2x = determination_Q1_Q2(PD1_2x, PD2_2x, PD3_2x)
Q1_3x, Q2_3x = determination_Q1_Q2(PD1_3x, PD2_3x, PD3_3x)
Q1_1z, Q2_1z = determination_Q1_Q2(PD1_1z, PD2_1z, PD3_1z)
Q1_2z, Q2_2z = determination_Q1_Q2(PD1_2z, PD2_2z, PD3_2z)
Q1_3z, Q2_3z = determination_Q1_Q2(PD1_3z, PD2_3z, PD3_3z)

Q1_list = np.array((Q1_1x, Q1_2x, Q1_3x, Q1_1z, Q1_2z, Q1_3z))
Q2_list = np.array((Q2_1x, Q2_2x, Q2_3x, Q2_1z, Q2_2z, Q2_3z))

if choices_dict["Q1_Q2_data"] == True:
    # This will save two 6xlen(Q1) np.arrays of all the relevant Q1 and Q2 values for each HoQI, in the order that these lists were constructed in the code on the two lines above here. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
    np.save('Endproduct_code/raw_Q1_data.npy', Q1_list)
    np.save('Endproduct_code/raw_Q2_data.npy', Q2_list)

## Single ellipse fitting Q1 and Q2
def residuals(params, x, y):
    x0, y0, a, b, theta = params
    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = - (x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    return xp ** 2 / a ** 2 + yp ** 2 / b ** 2 - 1

def transform(x, y, start_parameters=None):
    """
    Takes two np arrays (Q1, Q1) as input. You can also give starting paramaters by adding: start_parameters=[a, b, c, d, e]. Than the function
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

if choices_dict["single_ellipse_data"] == True:
    single_ellipse_Q1 = [0]*6
    single_ellipse_Q2 = [0]*6
    for i in range(0, 6):
        single_ellipse_Q1[i], single_ellipse_Q2[i] = transform(Q1_list[i, :], Q2_list[i, :])
    single_ellipse_Q1 = np.array(single_ellipse_Q1)
    single_ellipse_Q2 = np.array(single_ellipse_Q2)
    if choices_dict["Q1_Q2_data"] == True:
        # This will save two 6xlen(Q1) np.arrays of all the relevant Q1 and Q2 values for each HoQI, in the order that these lists were constructed in the code on the two lines above here. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
        np.save('Endproduct_code/single_ellipse_Q1_data.npy', single_ellipse_Q1)
        np.save('Endproduct_code/single_ellipse_Q2_data.npy', single_ellipse_Q2)

## Windowed ellipse fitting
def residuals(params, x, y):
    x0, y0, a, b, theta = params
    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = - (x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    return xp ** 2 / a ** 2 + yp ** 2 / b ** 2 - 1

def parameters_with_signal(x, y, start_parameters):
    """
    Input: Q1, Q2, starting parameters [x0, y0, a, b, theta]
    Output: [x0, y0, a, b, theta], [x0, y0, a, b, theta]
    This fits a given set Q1, Q2 with starting parameters
    """
    try:
        fit = least_squares(
            residuals,
            start_parameters,
            args=(x, y)
        )

        if not fit.success:
            return None, start_parameters

        vector = fit.x.copy()
        vector[2] = abs(vector[2])
        vector[3] = abs(vector[3])

        # theta beperken tot [0, pi)
        vector[4] = vector[4] % np.pi

        return vector, vector

    except ValueError:
        return None, start_parameters

def parameters_timeseries(x, y, window_size=None, step_size=None):
    """
    Input: Q1, Q2, window_size= , step_size=
    output: (N, 5) np array with N vectors where: vector = [x0, y0, a, b, theta]
    """

    if window_size is None:
        window_size = 250
    if step_size is None:
        step_size = 100
    # Start with an empty list and basic starting fit parameters
    vectoren = []
    fit_parameters = np.array([0, 0, 1, 1, 0])

    # For every window:
    for start in range(0, len(x) - window_size + 1, step_size):

        current_window_size = window_size


        while True:
            end = start + current_window_size
            if end > len(x):
                print(f"Geen grotere window meer mogelijk bij start={start}")
                break
            part_Q1 = x[start:end]
            part_Q2 = y[start:end]
            vector, new_fit_parameters = parameters_with_signal(
                part_Q1,
                part_Q2,
                start_parameters=fit_parameters
            )

            if vector is None:
                current_window_size += 50
                continue

            vector = np.ravel(vector)

            # Eerste fit altijd accepteren
            if len(vectoren) > 0:
                delta = np.array([0.2, 0.2, 0.5, 0.5])  # zonder theta

                lower_bounds = fit_parameters[:4] - delta
                upper_bounds = fit_parameters[:4] + delta

                lower_bounds[2] = max(lower_bounds[2], 0.001)
                lower_bounds[3] = max(lower_bounds[3], 0.001)

                if np.any(vector[:4] < lower_bounds) or np.any(vector[:4] > upper_bounds):
                    current_window_size += 50
                    print(
                        f"Fit buiten toegestane sprong bij start={start}, probeer opnieuw met "
                        f"window_size={current_window_size}"
                    )
                    continue

            fit_parameters = new_fit_parameters
            vectoren.append(np.ravel(vector))
            break
            
    vectoren = np.array(vectoren)

    # Repeat the parameters so almost every point has corresponding parameters (except for the last ones)
    return vectoren

def parameters(x, y, start_parameters=None):
    """
    Takes Q1 and Q2 data (np.array's) and spits out the fitting parameters
    the output is in the form of a 5-dim vector:
    (x0, y0, a, b, theta)
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
    if a > 10:
        raise ValueError("a > 10, kies een groter window_size")
    vector = np.column_stack((x0, y0, a, b, theta))
    start_parameters = [x0, y0, a, b, theta]
    return vector, start_parameters

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

# For this next part, you will unfortunatly have to experiment somewhat depending on which dataset you use, as the smallest window size that works differs between data sets. For now, they will be put at 500 datapoints as that should work on most normal datasets. To check if a windowsize works for a specific HoQI and dataset, make an ASD of the displacement of said HoQI, and if you lose all the relevant peaks, then the windowsize is to small.
if choices_dict["window_ellipse_data"] == True:
    Q1_windowed_ellipse = [0]*6
    Q2_windowed_ellipse = [0]*6
    window_sizes_list = [500, 500, 500, 300, 300, 300]
    step_size_list = [50, 50, 50, 50, 50, 50]
    for h in range(0,6):
        print("This is HoQI number: ", h)
        fitted_Q1, fitted_Q2 = variable_step_window_ellipse_fitting(Q1_list[h, :], Q2_list[h, :], window_size=window_sizes_list[h], step_size=step_size_list[h])
        Q1_windowed_ellipse[h] = fitted_Q1[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]
        Q2_windowed_ellipse[h] = fitted_Q2[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]  
    Q1_windowed_ellipse = np.array(Q1_windowed_ellipse)
    Q2_windowed_ellipse = np.array(Q2_windowed_ellipse)
    if choices_dict["Q1_Q2_data"] == True:
        # This will save two 6xlen(Q1) np.arrays of all the relevant Q1 and Q2 values for each HoQI, in the order that these lists were constructed in the code on the lines above here. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
        np.save('Endproduct_code/windowed_ellipse_Q1_data.npy', Q1_windowed_ellipse)
        np.save('Endproduct_code/windowed_ellipse_Q2_data.npy', Q2_windowed_ellipse)

## HoQI displacement lists
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

if choices_dict["raw_data"] == True:
    raw_HoQI_displacement = np.array([Q1_Q2_Length(Q1_list[0, :], Q2_list[0, :]), Q1_Q2_Length(Q1_list[1, :], Q2_list[1, :]), Q1_Q2_Length(Q1_list[2, :], Q2_list[2, :]), Q1_Q2_Length(Q1_list[3, :], Q2_list[3, :]), Q1_Q2_Length(Q1_list[4, :], Q2_list[4, :]), Q1_Q2_Length(Q1_list[5, :], Q2_list[5, :])])
    # This will save a 6xlen(Q1) np.array of all the relevant displacement values for each HoQI, in the order that these lists were constructed in the code on the line above here. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
    np.save('Endproduct_code/raw_HoQI_displacement_data.npy', raw_HoQI_displacement)

if choices_dict["single_ellipse_data"] == True:
    single_ellipse_HoQI_displacement = np.array([Q1_Q2_Length(single_ellipse_Q1[0, :], single_ellipse_Q2[0, :]), Q1_Q2_Length(single_ellipse_Q1[1, :], single_ellipse_Q2[1, :]), Q1_Q2_Length(single_ellipse_Q1[2, :], single_ellipse_Q2[2, :]), Q1_Q2_Length(single_ellipse_Q1[3, :], single_ellipse_Q2[3, :]), Q1_Q2_Length(single_ellipse_Q1[4, :], single_ellipse_Q2[4, :]), Q1_Q2_Length(single_ellipse_Q1[5, :], single_ellipse_Q2[5, :])])
    # This will save a 6xlen(Q1) np.array of all the relevant displacement values for each HoQI, in the order that these lists were constructed in the code on the line above here. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
    np.save('Endproduct_code/single_ellipse_HoQI_displacement_data.npy', single_ellipse_HoQI_displacement)

if choices_dict["window_ellipse_data"] == True:
    windowed_ellipse_HoQI_displacement = np.array([Q1_Q2_Length(Q1_windowed_ellipse[0, :], Q2_windowed_ellipse[0, :]), Q1_Q2_Length(Q1_windowed_ellipse[1, :], Q2_windowed_ellipse[1, :]), Q1_Q2_Length(Q1_windowed_ellipse[2, :], Q2_windowed_ellipse[2, :]), Q1_Q2_Length(Q1_windowed_ellipse[3, :], Q2_windowed_ellipse[3, :]), Q1_Q2_Length(Q1_windowed_ellipse[4, :], Q2_windowed_ellipse[4, :]), Q1_Q2_Length(Q1_windowed_ellipse[5, :], Q2_windowed_ellipse[5, :])])
    # This will save a 6xlen(Q1) np.array of all the relevant displacement values for each HoQI, in the order that these lists were constructed in the code on the line above here. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
    np.save('Endproduct_code/windowed_ellipse_HoQI_displacement_data.npy', windowed_ellipse_HoQI_displacement)

## DOF displacement lists
def transformation_matrix (ax, bx, cx, az, bz, cz):
    """
    transformation_matrix(np.array, np.array, np.array, np.array, np.array, np.array) -> np.array, np.array, np.array, np.array, np.array, np.array
    This function transforms from the HoQI displacement to the 6 degrees of freedom, 3 cartesian and 3 rotational.
    """
    R = 0.815

    x = (1/3) * (-2 * ax + bx + cx)
    y = (1/np.sqrt(3)) * (-bx + cx)
    z = (1/3) * (az + bz + cz)
    Rx = (1/(3*R)) * (2 * az - bz - cz)
    Ry = (1/(np.sqrt(3) * R)) * (bz - cz)
    Rz = (1/(3*R)) * (ax + bx + cx)

    return x, y, z, Rx, Ry, Rz

if choices_dict["raw_data"] == True:
    raw_DOF_displacement = transformation_matrix(raw_HoQI_displacement[0, :], raw_HoQI_displacement[1, :], raw_HoQI_displacement[2, :], raw_HoQI_displacement[3, :], raw_HoQI_displacement[4, :], raw_HoQI_displacement[5, :])
    # This will save a 6xlen(Q1) np.array of all the relevant displacement values for each DOF, in the order that these lists were constructed in is x, y, z, Rx, Ry, Rz. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
    np.save('Endproduct_code/raw_DOF_displacement_data.npy', raw_DOF_displacement)

if choices_dict["single_ellipse_data"] == True:
    single_ellipse_DOF_displacement = transformation_matrix(single_ellipse_HoQI_displacement[0, :], single_ellipse_HoQI_displacement[1, :], single_ellipse_HoQI_displacement[2, :], single_ellipse_HoQI_displacement[3, :], single_ellipse_HoQI_displacement[4, :], single_ellipse_HoQI_displacement[5, :])
    # This will save a 6xlen(Q1) np.array of all the relevant displacement values for each DOF, in the order that these lists were constructed in is x, y, z, Rx, Ry, Rz. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
    np.save('Endproduct_code/single_ellipse_DOF_displacement_data.npy', single_ellipse_DOF_displacement)

if choices_dict["window_ellipse_data"] == True:
    windowed_ellipse_DOF_displacement = transformation_matrix(windowed_ellipse_HoQI_displacement[0, :], windowed_ellipse_HoQI_displacement[1, :], windowed_ellipse_HoQI_displacement[2, :], windowed_ellipse_HoQI_displacement[3, :], windowed_ellipse_HoQI_displacement[4, :], windowed_ellipse_HoQI_displacement[5, :])
    # This will save a 6xlen(Q1) np.array of all the relevant displacement values for each DOF, in the order that these lists were constructed in is x, y, z, Rx, Ry, Rz. Each row of the np.array will thus be a specific HoQI, wheras each colum is a specific point in time
    np.save('Endproduct_code/windowed_ellipse_DOF_displacement_data.npy', windowed_ellipse_DOF_displacement)

## Parameter timeseries per HoQI
if choices_dict["ellipse_params_timeseries"] == True:
    np.save('Endproduct_code/HoQI_1x_ellipse_parameter_timeseries.npy', parameters_timeseries(Q1_list[0, :], Q2_list[0, :], window_size=1000, step_size=100))
    np.save('Endproduct_code/HoQI_2x_ellipse_parameter_timeseries.npy', parameters_timeseries(Q1_list[1, :], Q2_list[1, :], window_size=1000, step_size=100))
    np.save('Endproduct_code/HoQI_3x_ellipse_parameter_timeseries.npy', parameters_timeseries(Q1_list[2, :], Q2_list[2, :], window_size=1000, step_size=100))
    np.save('Endproduct_code/HoQI_1z_ellipse_parameter_timeseries.npy', parameters_timeseries(Q1_list[3, :], Q2_list[3, :], window_size=1000, step_size=100))
    np.save('Endproduct_code/HoQI_2z_ellipse_parameter_timeseries.npy', parameters_timeseries(Q1_list[4, :], Q2_list[4, :], window_size=1000, step_size=100))
    np.save('Endproduct_code/HoQI_3z_ellipse_parameter_timeseries.npy', parameters_timeseries(Q1_list[5, :], Q2_list[5, :], window_size=1000, step_size=100))