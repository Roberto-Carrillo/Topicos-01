import numpy as np
import pandas as pd
from scipy.spatial import distance

def calc_dist_2vectors(point1, point2):

    x_diff = np.square(point2.x_pos - point1.x_pos)
    y_diff = np.square(point2.y_pos - point1.y_pos)
    vectors_distance = np.sqrt(x_diff + y_diff)
    
    return vectors_distance

# Creación de función para calcular la longitud de la trayectoria
# Haciendo uso de la función creada anteriormente, vamos iterando sobre cada posición
# Y acumulando la suma de cada distancia entre el vector actual y el anterior
def create_traj_pl(trajectory_df):
    pl_distance_bm_df = np.array([
        calc_dist_2vectors(
            trajectory_df.iloc[i - 1],
            trajectory_df.iloc[i]
        ) for i in range(1, trajectory_df.shape[0])
    ])
    out_arr = np.cumsum(pl_distance_bm_df)
    out_df = pd.DataFrame()
    out_df["x_pos"] = np.arange(len(out_arr))
    out_df["y_pos"] = out_arr
    return out_df

# Function to calculate the displacement vector across n_step 
def calc_displacement_vec(trajectory, n_step):
    return np.array([
            np.square(distance.euclidean(trajectory.iloc[j], trajectory.iloc[j - n_step]))
        for j in range(n_step, len(trajectory))])

# Function to create the Mean Squared Displacement vector, looping through every t point in order to get the mean
# This result is saved into a numpy array creating the output vector
def create_traj_msd(trajectory):
    MSD_Out = np.empty(0)
    traj_length = trajectory.shape[0]
    for tau in range(1, traj_length):
        n_step = tau
        msd = np.mean(calc_displacement_vec(trajectory, n_step))
        MSD_Out = np.append(MSD_Out,msd)
    
    out_df = pd.DataFrame()
    out_df["x_pos"] = np.arange(len(MSD_Out))
    out_df["y_pos"] = MSD_Out
    return out_df

__all__= ["create_traj_pl", "create_traj_msd"]