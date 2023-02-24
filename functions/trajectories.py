import numpy as np
import pandas as pd

from scipy.stats import wrapcauchy
from scipy.stats import levy_stable
from .vec_2d import Vec2d


def create_brownian_trajectory(start_pos, n_steps):

    # Creamos un arreglo de 2 vectores de n_steps de longitud, y asignamos
    # la posición inicial en la primera pocisión de cada vector
    out = np.zeros((2, n_steps))
    out[0] = start_pos[0]
    out[1] = start_pos[1]

    for curr_step in range(1, n_steps):

        # Definimos una dirección que tiene uniforme probabilidad de moverse
        # en alguna de las 4 direcciones, y definimos la posición anterior como referencia
        direction = np.random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        prev_x = out[0][curr_step - 1]
        prev_y = out[1][curr_step - 1]

        # Asignamos el valor de la nueva trayectoria añadiendo el valor de la posición previa
        if (direction == "UP"):
            out[0][curr_step] = prev_x
            out[1][curr_step] = prev_y + 1
        elif (direction == "DOWN"):
            out[0][curr_step] = prev_x
            out[1][curr_step] = prev_y - 1
        elif (direction == "LEFT"):
            out[0][curr_step] = prev_x - 1
            out[1][curr_step] = prev_y
        else:
            out[0][curr_step] = prev_x + 1
            out[1][curr_step] = prev_y

    return out


def create_crw_trajectory(start_pos=(0, 0), n_steps=1000, coeficient=0.5):
    # Inicializando vector de velocidad
    velocity = Vec2d(coeficient, 0)
    # Creando matriz para el caminado aleatorio, y distribución de pasos
    turn_angle_dist = np.array(wrapcauchy.rvs(coeficient, size=n_steps))
    BM_2d = np.ones(shape=(n_steps, 2)) * start_pos

    for i in range(1, n_steps):

        # Use wrapCauchy to generate random number
        turn_angle = turn_angle_dist[i]
        # Girar el vector de velocidad
        velocity = velocity.rotated(turn_angle)

        # Desplazamiento con el vector
        BM_2d[i, 0] = BM_2d[i-1, 0] + velocity.x
        BM_2d[i, 1] = BM_2d[i-1, 1] + velocity.y
    return BM_2d

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
