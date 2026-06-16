import numpy as np

# the transformation matrix for HoQI 1x
matrix_1x = np.array([
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0],
    [0, 0, 0, 1, 0, 0]])

# the transformation matrix for HoQI 1z
matrix_1z = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]])

# the transformation matrix for HoQI 2x
matrix_2x = np.array([
    [np.sqrt(1/3), 0, -np.sqrt(1/3), 0, 0, 0],
    [0, 0, 0, 0, 1, 0]])

# the transformation matrix for HoQI 2z
matrix_2z = np.array([
    [0, 1, 0, 0, 0, 0],
    [np.sqrt(1/3), 0, -np.sqrt(1/3), 0, 0, 0]])

# the transformation matrix for HoQI 3x
matrix_3x = np.array([
    [-np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1]])

# the transformation matrix for HoQI 3z
matrix_3z = np.array([
    [0, 0, 1, 0, 0, 0],
    [-np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0, 0]])