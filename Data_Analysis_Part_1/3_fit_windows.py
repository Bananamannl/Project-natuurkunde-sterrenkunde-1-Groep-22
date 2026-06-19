import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from gwpy.timeseries import TimeSeries

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

## Getting Q1 and Q2 raw
Q1_list = np.array([np.load('Data_Analysis_Part_1/1xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/2xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/3xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/1zQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/2zQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/3zQ1.npy')[:3000000]])

Q2_list = np.array([np.load('Data_Analysis_Part_1/1xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/2xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/3xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/1zQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/2zQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/3zQ2.npy')[:3000000]])

## Calculating Q1 and Q2 for seperate window sizes

Q1_windowed_ellipse_1000 = [0]*6
Q2_windowed_ellipse_1000 = [0]*6
window_sizes_list = [1000, 1000, 1000, 1000, 1000, 1000]
step_size_list = [1000, 1000, 1000, 1000, 1000, 1000]
for h in range(0,6):
    print("This is HoQI number: ", h)
    fitted_Q1, fitted_Q2 = variable_step_window_ellipse_fitting(Q1_list[h, :], Q2_list[h, :], window_size=window_sizes_list[h], step_size=step_size_list[h])
    Q1_windowed_ellipse_1000[h] = fitted_Q1[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]
    Q2_windowed_ellipse_1000[h] = fitted_Q2[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]  
Q1_windowed_ellipse_1000 = np.array(Q1_windowed_ellipse_1000)
Q2_windowed_ellipse_1000 = np.array(Q2_windowed_ellipse_1000)

Q1_windowed_ellipse_500 = [0]*6
Q2_windowed_ellipse_500 = [0]*6
window_sizes_list = [500, 500, 500, 300, 500, 300]
step_size_list = [50, 50, 50, 50, 100, 50]
for h in range(0,6):
    print("This is HoQI number: ", h)
    fitted_Q1, fitted_Q2 = variable_step_window_ellipse_fitting(Q1_list[h, :], Q2_list[h, :], window_size=window_sizes_list[h], step_size=step_size_list[h])
    Q1_windowed_ellipse_500[h] = fitted_Q1[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]
    Q2_windowed_ellipse_500[h] = fitted_Q2[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]  
Q1_windowed_ellipse_500 = np.array(Q1_windowed_ellipse_500)
Q2_windowed_ellipse_500 = np.array(Q2_windowed_ellipse_500)

Q1_windowed_ellipse_500_300_50 = [0]*6
Q2_windowed_ellipse_500_300_50 = [0]*6
window_sizes_list = [500, 500, 500, 300, 300, 300]
step_size_list = [50, 50, 50, 50, 50, 50]
for h in range(0,6):
    print("This is HoQI number: ", h)
    fitted_Q1, fitted_Q2 = variable_step_window_ellipse_fitting(Q1_list[h, :], Q2_list[h, :], window_size=window_sizes_list[h], step_size=step_size_list[h])
    Q1_windowed_ellipse_500_300_50[h] = fitted_Q1[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]
    Q2_windowed_ellipse_500_300_50[h] = fitted_Q2[0 : (len(Q1_list[h, :]) - 2*max(window_sizes_list))]  
Q1_windowed_ellipse_500_300_50 = np.array(Q1_windowed_ellipse_500_300_50)
Q2_windowed_ellipse_500_300_50 = np.array(Q2_windowed_ellipse_500_300_50)

## Calculation HoQI displacement
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

windowed_ellipse_HoQI_displacement_1000 = np.array([Q1_Q2_Length(Q1_windowed_ellipse_1000[0, :], Q2_windowed_ellipse_1000[0, :]), Q1_Q2_Length(Q1_windowed_ellipse_1000[1, :], Q2_windowed_ellipse_1000[1, :]), Q1_Q2_Length(Q1_windowed_ellipse_1000[2, :], Q2_windowed_ellipse_1000[2, :]), Q1_Q2_Length(Q1_windowed_ellipse_1000[3, :], Q2_windowed_ellipse_1000[3, :]), Q1_Q2_Length(Q1_windowed_ellipse_1000[4, :], Q2_windowed_ellipse_1000[4, :]), Q1_Q2_Length(Q1_windowed_ellipse_1000[5, :], Q2_windowed_ellipse_1000[5, :])])

windowed_ellipse_HoQI_displacement_500 = np.array([Q1_Q2_Length(Q1_windowed_ellipse_500[0, :], Q2_windowed_ellipse_500[0, :]), Q1_Q2_Length(Q1_windowed_ellipse_500[1, :], Q2_windowed_ellipse_500[1, :]), Q1_Q2_Length(Q1_windowed_ellipse_500[2, :], Q2_windowed_ellipse_500[2, :]), Q1_Q2_Length(Q1_windowed_ellipse_500[3, :], Q2_windowed_ellipse_500[3, :]), Q1_Q2_Length(Q1_windowed_ellipse_500[4, :], Q2_windowed_ellipse_500[4, :]), Q1_Q2_Length(Q1_windowed_ellipse_500[5, :], Q2_windowed_ellipse_500[5, :])])

windowed_ellipse_HoQI_displacement_500_300_50 = np.array([Q1_Q2_Length(Q1_windowed_ellipse_500_300_50[0, :], Q2_windowed_ellipse_500_300_50[0, :]), Q1_Q2_Length(Q1_windowed_ellipse_500_300_50[1, :], Q2_windowed_ellipse_500_300_50[1, :]), Q1_Q2_Length(Q1_windowed_ellipse_500_300_50[2, :], Q2_windowed_ellipse_500_300_50[2, :]), Q1_Q2_Length(Q1_windowed_ellipse_500_300_50[3, :], Q2_windowed_ellipse_500_300_50[3, :]), Q1_Q2_Length(Q1_windowed_ellipse_500_300_50[4, :], Q2_windowed_ellipse_500_300_50[4, :]), Q1_Q2_Length(Q1_windowed_ellipse_500_300_50[5, :], Q2_windowed_ellipse_500_300_50[5, :])])

## ASD plot
segment_time_set = 1000
fs_set = 1000
window = 50

def get_asd(data, fs, segment_time):
    """
    get_asd(np.array, int, int) -> FrequencySeries
    Takes a list of displacements and outputs a spectral density diagram for said displacement. fs is the sample rate per second, and segment_time is the amount of seconds your dataset covers. 
    """
    data = np.asarray(data)
    data = data - np.mean(data) 
    ts = TimeSeries(data, sample_rate=fs)
    ASD = ts.asd(segment_time, overlap=segment_time/2) 
    return ASD

names_list = ['1x', '2x', '3x', '1z', '2z', '3z']

figure, axes = plt.subplots(2, 3)
for i in range(0,2):
    for j in range(0,3):
        asd_1000 = get_asd(windowed_ellipse_HoQI_displacement_1000[i*3+j, :], fs_set, segment_time_set)
        asd_1000_smooth = np.convolve(asd_1000.value, np.ones(window)/window, mode='same')
        asd_500 = get_asd(windowed_ellipse_HoQI_displacement_500[i*3+j, :], fs_set, segment_time_set)
        asd_500_smooth = np.convolve(asd_500.value, np.ones(window)/window, mode='same')
        asd_500_300_50 = get_asd(windowed_ellipse_HoQI_displacement_500_300_50[i*3+j, :], fs_set, segment_time_set)
        asd_500_300_50_smooth = np.convolve(asd_500_300_50.value, np.ones(window)/window, mode='same')

        axes[i, j].set_ylabel('Gain')
        axes[i, j].set_xlabel('Frequency (Hz)')
        axes[i, j].loglog(asd_500_300_50.frequencies.value, asd_500_300_50_smooth, 'g')
        axes[i, j].loglog(asd_1000.frequencies.value, asd_1000_smooth, 'r')
        axes[i, j].loglog(asd_500.frequencies.value, asd_500_smooth, 'b')
        axes[i, j].set_title(names_list[i*3+j])
        axes[i, j].grid(True, which="both")


plt.subplots_adjust(hspace=0.312)
figure.set_figheight(8)
figure.set_figwidth(16)
plt.show()