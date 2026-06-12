import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from ellipse_parameters import *
import matplotlib.pyplot as plt 
from orthogonal_matrices import *


def expand_window_parameters(parameters, window_size):
    """
    input= (parameters, window_size)
    output= lijst die elke parameter voor de hele window herhaald
    """
    return np.repeat(parameters, window_size, axis=0)

def keep_recent_data(X_train, y_train, memory_size):
    """
    Houdt alleen de laatste memory_size datapunten in de training set.
    """
    if len(X_train) > memory_size:
        X_train = X_train[-memory_size:]
        y_train = y_train[-memory_size:]
    
    return X_train, y_train


def rolling_knn_predict_points(
    positions,
    parameters,
    train_points=10000,
    window_size=250,
    memory=20000):

    model = make_pipeline(
        StandardScaler(),
        KNeighborsRegressor(
            n_neighbors=200,
            weights="distance",
            p=1
        )
    )
    param_all = expand_window_parameters(parameters, window_size)

    # zorg dat positions en y_all even lang zijn
    N = min(len(positions), len(param_all))
    X_all = positions[:N]
    y_all = param_all[:N]

    X_train = X_all[:train_points]
    y_train = y_all[:train_points]

    model.fit(X_train, y_train)

    predictions = []

    for start in range(train_points, N, window_size):
        end = start + window_size

        X_window = X_all[start:end]
        y_window = y_all[start:end]

        # voorspel elk punt in deze window
        pred_window = model.predict(X_window)
        predictions.append(pred_window)

        #voeg de nieuwe window toe aan de trainingdata
        X_train = np.vstack([X_train, X_window])
        y_train = np.vstack([y_train, y_window])

        X_train, y_train = keep_recent_data(X_train, y_train, memory)

        #train het model opnieuw
        model.fit(X_train, y_train)

    return np.vstack(predictions)

def transform_with_parameters(Q1, Q2, parameters):
    Q1, Q2 = Q1[10000:], Q2[10000:]
    vectors = np.column_stack((Q1, Q2))
    Q_transformed = []
    for i in range(0, len(Q1)):
        x0, y0, a, b, theta = parameters[i, :5]
        centre = np.array([x0, y0])
        squeeze = np.array([a, b])
        R = np.array([[np.cos(theta), - np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]])
        centred = vectors[i] - centre
        rotated = centred @ R 
        unit_vector = rotated / squeeze
        Q_transformed.append(unit_vector)
    Q_transformed = np.array(Q_transformed)
    return Q_transformed[:, 0], Q_transformed[:, 1]


Q1, Q2 = np.load("Data_Analysis_Part_1\\3xQ1.npy"), np.load("Data_Analysis_Part_1\\3xQ2.npy")
# Q1, Q2 = Q1[1700000:2300000], Q2[1700000:2300000]
HoQIs = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
# HoQIs = HoQIs[1700000:2300000]



start = 0
end = 1000000

orth_plane = HoQIs[:end] @ matrix_3x.T
# orth_plane = HoQIs @ matrix_3x.T
Q1, Q2 = Q1[:end], Q2[:end]
parameters = parameters_timeseries(Q1, Q2, window_size=500, step_size=500)

tested_parameters = rolling_knn_predict_points(orth_plane, parameters, window_size=500)

Q1_new, Q2_new = transform_with_parameters(Q1, Q2, tested_parameters)
kleur = np.arange(len(Q1_new[start:end]))

plt.figure()
plt.scatter(Q1_new[start:end], Q2_new[start:end], c=kleur, s=3, cmap="viridis")
plt.colorbar(label="Datapunt index")
plt.axis("equal") 
plt.grid()
plt.show()


# Q1, Q2 = np.load("Data_Analysis_Part_1\\3xQ1.npy"), np.load("Data_Analysis_Part_1\\3xQ2.npy")
# HoQIs = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
# orth_plane = HoQIs @ matrix_3x.T

# parameters = parameters_timeseries(Q1, Q2, window_size=250, step_size=250)

# tested_parameters = rolling_knn_predict_points(orth_plane, parameters)
# Q1_new, Q2_new = transform_with_parameters(Q1, Q2, tested_parameters)