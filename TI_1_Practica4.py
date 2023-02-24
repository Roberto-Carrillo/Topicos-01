import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image
from functions import plots
from functions.streamlit_helpers import load_text



st.set_page_config(page_title="Dashboard - Tópicos de Industria 1", 
                    page_icon=":chart_with_upwards_trend:",
                    layout="wide",
                    initial_sidebar_state="expanded")

# --- Data Loading ----
# @st.cache
# def get_data():
    

# --- Header Section ----
reduce_header_height_style = """<style>div.block-container {padding-top:2rem;}</style>"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)
header_component = load_text('ui/header.html')
components.html(header_component)

trajectory_df = None
trajectory_df = pd.read_csv('trajectories/brownian_3.csv')
metrics_df = pd.read_csv('metrics/met_df_2.csv')

# with header_mid:

with st.sidebar:
    with st.container():
        st.subheader("Parámetros")
        traj_type = st.radio("Tipo de Trayectoria", ('Brownian Motion', 'Lévy Flight', 'Correlated Random Walk'))
        steps = st.number_input("Número de pasos", min_value=10, max_value=20000)
        col1, col2 = st.columns(2)

        with col1:
            x_initial_pos = st.number_input("Inicio - X")
        with col2:
            y_initial_pos = st.number_input("Inicio - Y")
        
        if traj_type == 'Brownian Motion':
            bm_speed = st.slider("Velocidad", min_value=0.1, max_value=5.0, value=0.1)
        elif traj_type == 'Lévy Flight':
            lf_alpha = st.slider("Exponente Levy (alpha)", min_value=0.1, max_value=5.0, value=0.1)
            lf_beta = st.slider("Exponente simetría (beta)", min_value=0.1, max_value=5.0, value=0.1)
        else:
            crw_exp = st.slider("Velocidad", min_value=0.1, max_value=5.0, value=0.1)
        metrics_type = st.radio("Tipo de Métricas", ('Longitud de trayectoria', 'Media cuadrada de desplazamiento', 'Ambas'))

# with st.expander("Ver más detalles"):

#     if traj_type == 'Brownian Motion':
#         st.markdown('''
#             ### Movimiento Browniano
#             Es un tipo de movimiento aleatorio uniforme
#         ''')
#         header = load_text('header.md')
#         st.write(header)


traj_plot_3d, traj_metrics_2d = st.columns([1,1], gap="large")

fig_traj_3d = go.Figure()
fig_metr_2d = go.Figure()

with traj_plot_3d:
    st.subheader("Gráfica 3D de Trayectoria")
    plots.add_3d_line_trace(
        target=fig_traj_3d,
        x = trajectory_df.x_pos,
        y = trajectory_df.y_pos,
        z = trajectory_df.index,
        trace_name = 'BM 2D Trajectory'
    )
    st.plotly_chart(fig_traj_3d, use_container_width=True)
with traj_metrics_2d:
    st.subheader("Gráfica de Métricas")
    plots.add_2d_line_trace(
        target=fig_metr_2d,
        x = metrics_df.index,
        y = metrics_df.MSD_BM,
        trace_name="BM MSD"
    )
    st.plotly_chart(fig_metr_2d, use_container_width=True)