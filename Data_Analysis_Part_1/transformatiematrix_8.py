import numpy as np
import matplotlib as mt

# function to transform the measured displacements into the actual displacements in all six degrees of freedom
# note that this function uses lists as input arguments
def transformatiematrix (ax, bx, cx, az, bz, cz):
    R = 0.815

    x = (1/3) * (-2 * ax + bx + cx)
    y = (1/np.sqrt(3)) * (-bx + cx)
    z = (1/3) * (az + bz + cz)
    Rx = (1/(3*R)) * (2 * az - bz - cz)
    Ry = (1/(np.sqrt(3) * R)) * (bz - cz)
    Rz = (1/(3*R)) * (ax + bx + cx)

    return x, y, z, Rx, Ry, Rz