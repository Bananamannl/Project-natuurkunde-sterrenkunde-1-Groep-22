import numpy as np
import matplotlib as mt
from arctan_Q1_Q2_5_6_7 import Q1_Q2_Length
from bepaling_Q1_Q2_2 import Q_lijst

Q1_1x = Q_lijst[0] 
Q2_1x = Q_lijst[1]
Q1_2x = Q_lijst[2]
Q2_2x = Q_lijst[3]
Q1_3x = Q_lijst[4]
Q2_3x = Q_lijst[5]
Q1_1z = Q_lijst[6]
Q2_1z = Q_lijst[7]
Q1_2z = Q_lijst[8]
Q2_2z = Q_lijst[9]
Q1_3z = Q_lijst[10]
Q2_3z = Q_lijst[11]

length_1x_lijst = []
for i in range(0, len(Q1_1x)):
    length_1x_HoQI = Q1_Q2_Length(Q1_1x[i], Q2_1x[i])
    length_1x_lijst.append(length_1x_HoQI)

length_2x_lijst = []
for j in range(0, len(Q1_2x)):
    length_2x_HoQI = Q1_Q2_Length(Q1_2x[j], Q2_2x[j])
    length_2x_lijst.append(length_2x_HoQI)

length_3x_lijst = []
for k in range(0, len(Q1_3x)):
    length_3x_HoQI = Q1_Q2_Length(Q1_3x[k], Q2_3x[k])
    length_3x_lijst.append(length_3x_HoQI)

length_1z_lijst = []
for l in range(0, len(Q1_1z)):
    length_1z_HoQI = Q1_Q2_Length(Q1_1z[l], Q2_1z[l])
    length_1z_lijst.append(length_1z_HoQI)

length_2z_lijst = []
for m in range(0, len(Q1_2z)):
    length_2z_HoQI = Q1_Q2_Length(Q1_2z[m], Q2_2z[m])
    length_2z_lijst.append(length_2z_HoQI)

length_3z_lijst = []
for n in range(0, len(Q1_3z)):
    length_3z_HoQI = Q1_Q2_Length(Q1_3z[n], Q2_3z[n])
    length_3z_lijst.append(length_3z_HoQI)

R = 0.815
def transoformatiematrix (ax, bx, cx, az, bz, cz):
    x = (1/3) * (-ax + 2 * bx + 2 * cx)
    y = (1/2) * (-2 * (1/np.sqrt(3)) * bx + 2 * (1/np.sqrt(3)) * cx)
    z = (1/3) * (az + bz + cz)
    Rx = (2/(3*R)) * (az - (1/2) * bz -(1/2) * cz)
    Ry = (1/(np.sqrt(3) * R)) * (bz - cz)
    Rz = (1/(3*R)) * (ax + bx + cx)
    return x, y, z, Rx, Ry, Rz

x_lijst = []
y_lijst = []
z_lijst = []
Rx_lijst = []
Ry_lijst = []
Rz_lijst = []

def displacement_dof():
    for o in range(0, len(Q1_1x)):
        x, y, z, Rx, Ry, Rz = transoformatiematrix(length_1x_lijst[o], length_2x_lijst[o], length_3x_lijst[o], length_1z_lijst[o], length_2z_lijst[o], length_3z_lijst[o])
        x_lijst.append(x)
        y_lijst.append(y)
        z_lijst.append(z)
        Rx_lijst.append(Rx)
        Ry_lijst.append(Ry)
        Rz_lijst.append(Rz)
    return displacement_dof