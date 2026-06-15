import numpy as np
from knn_functions import *
from functions import *
from windowed_ellipse_fitting import standard_step_window_ellipse_fitting

#begin met allenn Q lijsten te importeren
Q1_1x, Q2_1x = np.load("Data_Analysis_Part_1\\1xQ1.npy"), np.load("Data_Analysis_Part_1\\1xQ2.npy")
Q1_2x, Q2_2x = np.load("Data_Analysis_Part_1\\2xQ1.npy"), np.load("Data_Analysis_Part_1\\2xQ2.npy")
Q1_3x, Q2_3x = np.load("Data_Analysis_Part_1\\3xQ1.npy"), np.load("Data_Analysis_Part_1\\3xQ2.npy")
Q1_1z, Q2_1z = np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")
Q1_2z, Q2_2z = np.load("Data_Analysis_Part_1\\2zQ1.npy"), np.load("Data_Analysis_Part_1\\2zQ2.npy")
Q1_3z, Q2_3z = np.load("Data_Analysis_Part_1\\3zQ1.npy"), np.load("Data_Analysis_Part_1\\3zQ2.npy")
data_size = len(Q1_1x)
#10.000 punten parameters fitten
Q_lijst = [[Q1_1x, Q2_1x], 
           [Q1_2x, Q2_2x], 
           [Q1_3x, Q2_3x], 
           [Q1_1z, Q2_1z], 
           [Q1_2z, Q2_2z], 
           [Q1_3z, Q2_3z]]
windows = [500, 500, 210, 250, 250, 250]
initial_training_size = 10500

transformed_Q_lijst = []
parameters_lijst = []
predicted_parameters_lijst = []

for index, Q in enumerate(Q_lijst):
    Q1 = Q[0]
    Q2 = Q[1]
    windows_size = windows[index]

    Q1_transformed, Q2_transformed = standard_step_window_ellipse_fitting(Q1[:initial_training_size], 
                                                                          Q2[:initial_training_size], 
                                                                          window_size=windows_size)
    
    transformed_Q_lijst.append([Q1_transformed, Q2_transformed])

    parameters = parameters_timeseries(Q[0][:initial_training_size], 
                                       [1][:initial_training_size], 
                                       window_size=windows_size, 
                                       step_size=windows_size)
    parameters_lijst.append(parameters)

for index, Q in enumerate(Q_lijst):
    window_size = windows[index]
    Q1 = Q[0]
    Q2 = Q[1]

    for number in range(0, data_size - initial_training_size, window_size):
        predicted_parameters = rolling_knn_predict_points(Q1[:initial_training_size + number + window_size], 
                                   Q2[:initial_training_size + number + window_size], 
                                   train_points=initial_training_size + number, 
                                   window_size=window_size)
        transformed_data_chunk = transform_with_parameters(Q1[initial_training_size + number:initial_training_size + number + window_size],
                                  Q2[initial_training_size + number:initial_training_size + number + window_size],
                                  predicted_parameters)
        