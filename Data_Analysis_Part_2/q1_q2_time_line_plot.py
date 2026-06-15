import numpy as np
import matplotlib.pyplot as plt
from functions import *

def plot_q1_q2_3d(Q1, Q2, transform=None, transform_data=False):
    """
    Plot Q1 en Q2 als 3D traject over tijd.

    Parameters:
    -----------
    file_q1 : str
        Pad naar Q1 .npy bestand
    file_q2 : str
        Pad naar Q2 .npy bestand
    transform : function, optional
        Functie die (Q1, Q2) -> (Q1, Q2) transformeert
    transform_data : bool
        Als True wordt transform toegepast
    """

    # check lengte
    if len(Q1) != len(Q2):
        raise ValueError("Q1 en Q2 moeten dezelfde lengte hebben")

    # optionele transformatie
    if transform_data:
        if transform is None:
            raise ValueError("transform_data=True maar geen transform functie meegegeven")
        Q1, Q2 = transform(Q1, Q2)

    # tijdas (1 ms stappen)
    dt = 1 / 1000
    t = np.arange(len(Q1)) * dt

    # 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(Q1, Q2, t, linewidth=1)

    ax.set_xlabel("Q1")
    ax.set_ylabel("Q2")
    ax.set_zlabel("Time (s)")

    plt.title("Q1-Q2 traject in de tijd")
    plt.show()

# Q1, Q2 = np.load("Data_Analysis_Part_1\\1xQ1.npy"), np.load("Data_Analysis_Part_1\\1xQ2.npy")
# plot_q1_q2_3d(
#     Q1[1820000:1830000], Q2[1820000:1830000], transform= True
# )

Q1, Q2 = np.load("Data_Analysis_Part_1\\3zQ1.npy"), np.load("Data_Analysis_Part_1\\3zQ2.npy")
plot_q1_q2_3d(
    Q1[140000:142000], Q2[140000:142000],  transform=True
)
