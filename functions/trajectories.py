import numpy as np
import pandas as pd

from scipy.stats import wrapcauchy
from scipy.stats import levy_stable
from .vec_2d import Vec2d


def create_brownian_trajectory(start_pos=[0,0], n_steps=1000, speed = 0.5):

    velocity = Vec2d(speed, 0)
    #Init DF
    BM_2d_df = pd.DataFrame(columns=['x_pos', 'y_pos'])
    temp_df = pd.DataFrame([{ 
        'x_pos': start_pos[0], 
        'y_pos': start_pos[1], 
    }])

    BM_2d_df = pd.concat([BM_2d_df, temp_df], ignore_index=True)

    for i in range(n_steps - 1):
        #turn_angle = np.random.choice([0, np.pi/2, np.pi, 3*np.pi/2])
        turn_angle = np.random.uniform(low=-np.pi, high=np.pi)
        velocity = velocity.rotated(turn_angle)
        temp_df = pd.DataFrame([{
            'x_pos': BM_2d_df.x_pos[i] + velocity.x,
            'y_pos': BM_2d_df.y_pos[i] + velocity.y
        }])
        BM_2d_df = pd.concat([BM_2d_df, temp_df], ignore_index=True)
    
    return BM_2d_df


def create_crw_trajectory(start_pos=(0, 0), n_steps=1000, crw_exp=0.5):
    vector = Vec2d(crw_exp, 0)
    crw_2d_df = pd.DataFrame(columns=['x_pos', 'y_pos'])
    temp_df = pd.DataFrame([{ 'x_pos': start_pos[0], 'y_pos': start_pos[1] }])
    crw_2d_df = pd.concat([crw_2d_df, temp_df], ignore_index=True)
    cauchy_rvs = np.array(wrapcauchy.rvs(crw_exp, size=n_steps))

    for i in range(n_steps - 1):
        next_pos =  vector.rotated(cauchy_rvs[i])
        next_pos_df = pd.DataFrame([{
            'x_pos': crw_2d_df.x_pos[i] + next_pos.x,
            'y_pos': crw_2d_df.y_pos[i] + next_pos.y
        }])
        crw_2d_df = pd.concat([crw_2d_df, next_pos_df], ignore_index=True)
    
    return crw_2d_df

# Definición de Función para generar trayectoria


def create_levy_trajectory(start_pos=[0, 0], n_steps=500, levy_exp=0.5, beta=0):

    # Init output dataframe with their corresponding names and start position
    levy_2d_df = pd.DataFrame(columns=['x_pos', 'y_pos'])
    temp_df = pd.DataFrame([{
        'x_pos': start_pos[0],
        'y_pos': start_pos[1],
    }])
    levy_2d_df = pd.concat([levy_2d_df, temp_df], ignore_index=True)

    # Create two random value samples:
    #   - We need a wrapcauchy sample to calculate the angle for the sample
    #   - A levy rvs to determine the step length
    angle = np.array(wrapcauchy.rvs(0.5, size=n_steps))
    levy_rvs = np.array(levy_stable.rvs(levy_exp, beta, size=n_steps))

    for i in range(n_steps - 1):
        # Create angle of rotation with the angle defined above using the rotated helper from Vec2d

        # Vector
        vector = Vec2d(levy_exp, 0)
        next_pos = vector.rotated(angle[i])
        next_step = np.abs(levy_rvs[i])

        # Add coordinates to temporary dataframe, adding the previous position with the new position,
        # as well as add the corresponding step length to the position
        next_pos_df = pd.DataFrame([{
            'x_pos': levy_2d_df.x_pos[i] + (next_step * next_pos.x),
            'y_pos': levy_2d_df.y_pos[i] + (next_step * next_pos.y)
        }])
        # Concatenate old coordinates with new coordinates
        levy_2d_df = pd.concat([levy_2d_df, next_pos_df], ignore_index=True)

    return levy_2d_df

__all__ = ["create_brownian_trajectory", "create_levy_trajectory", "create_crw_trajectory"]