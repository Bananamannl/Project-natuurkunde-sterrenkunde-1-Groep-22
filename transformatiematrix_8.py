import numpy as np
import matplotlib as mt
from arctan_Q1_Q2_5_6_7 import Q1_Q2_Length
from bepaling_Q1_Q2_2 import Q_lijsten

Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('1xQ1.npy'), np.load('1xQ2.npy'), np.load('2xQ1.npy'), np.load('2xQ2.npy'), np.load('3xQ1.npy'), np.load('3xQ2.npy'), np.load('1zQ1.npy'), np.load('1zQ2.npy'), np.load('2zQ1.npy'), np.load('2zQ2.npy'), np.load('3zQ1.npy'), np.load('3zQ2.npy')

length_1x_lijst = Q1_Q2_Length(Q1_1x, Q2_1x)

length_2x_lijst = Q1_Q2_Length(Q1_2x, Q2_2x)

length_3x_lijst = Q1_Q2_Length(Q1_3x, Q2_3x)

length_1z_lijst = Q1_Q2_Length(Q1_1z, Q2_1z)

length_2z_lijst = Q1_Q2_Length(Q1_2z, Q2_2z)

length_3z_lijst = Q1_Q2_Length(Q1_3z, Q2_3z)

R = 0.815
def transoformatiematrix (ax, bx, cx, az, bz, cz):
    x = (1/3) * (-ax + 2 * bx + 2 * cx)
    y = (1/2) * (-2 * (1/np.sqrt(3)) * bx + 2 * (1/np.sqrt(3)) * cx)
    z = (1/3) * (az + bz + cz)
    Rx = (2/(3*R)) * (az - (1/2) * bz -(1/2) * cz)
    Ry = (1/(np.sqrt(3) * R)) * (bz - cz)
    Rz = (1/(3*R)) * (ax + bx + cx)
    return x, y, z, Rx, Ry, Rz

x_lijst, y_lijst, z_lijst, Rx_lijst, Ry_lijst, Rz_lijst  = transoformatiematrix(length_1x_lijst, length_2x_lijst, length_3x_lijst, length_1z_lijst, length_2z_lijst, length_3z_lijst)
 