import numpy as np
import matplotlib.pyplot as plt
from data_2_functions import *

Q1_list = np.load('Dataset_2_Analaysis/Data2_Q1.npy')
Q2_list = np.load('Dataset_2_Analaysis/Data2_Q2.npy')

transformed_Q1_list = [0]*6
transformed_Q2_list = [0]*6
for i in range(0,6):
    Q1_temp, Q2_temp = transform(Q1_list[i, : ], Q2_list[i, : ])
    transformed_Q1_list[i] = Q1_temp
    transformed_Q2_list[i] = Q2_temp

