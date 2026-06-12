import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from ellipse_parameters import *
import matplotlib.pyplot as plt 

matrix_1z = np.array([
    [-2/3, 1/3, 1/3, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]
])

Q1, Q2 = np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")
Q1, Q2 = Q1[:1000000], Q2[:1000000]
HoQIs = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
HoQIs = HoQIs[:1000000]

orth_plane = HoQIs @ matrix_1z.T
parameters = parameters_timeseries(Q1, Q2, window_size=250, step_size=250)
# parameters = parameters[0:5, :]

def expand_window_parameters(parameters, window_size):
    """
    input= (parameters, window_size)
    output= lijst die elke parameter voor de hele window herhaald
    """
    return np.repeat(parameters, window_size, axis=0)

def rolling_knn_predict_points(
    positions,
    parameters,
    train_points=10000,
    window_size=250):

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

        #train het model opnieuw
        model.fit(X_train, y_train)

    return np.vstack(predictions)

tested_parameters = rolling_knn_predict_points(orth_plane, parameters)


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

Q1_new, Q2_new = transform_with_parameters(Q1, Q2, tested_parameters)

plt.figure()
plt.scatter(Q1_new, Q2_new, s=3)
plt.axis("equal") 
plt.grid()
plt.show()