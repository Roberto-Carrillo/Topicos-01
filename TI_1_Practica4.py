import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image
from functions import plots, trajectories
from functions import streamlit_helpers as sh



st.set_page_config(page_title="Dashboard - Tópicos de Industria 1", 
                    page_icon=":chart_with_upwards_trend:",
                    layout="wide",
                    initial_sidebar_state="expanded")

# --- Data Loading ----
st.session_state.trajectory_df = None
st.session_state.metrics_df = None

# --- Header Section ----
reduce_header_height_style = """<style>div.block-container {padding-top:2rem;}</style>"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)
header_component = sh.load_text('ui/header.html')
components.html(header_component)

# with header_mid:

with st.sidebar:
    with st.container():
        st.subheader("Parámetros")
        traj_type = st.radio("Tipo de Trayectoria", ('Brownian Motion', 'Lévy Flight', 'Correlated Random Walk'), key="traj_type")
        n_steps = st.number_input("Número de pasos", min_value=10, max_value=20000, value=1000, key="n_steps")
        col1, col2 = st.columns(2)

        with col1:
            x_initial_pos = st.number_input("Inicio - X", value=0.0, key="x_initial_pos")
        with col2:
            y_initial_pos = st.number_input("Inicio - Y", value=0.0, key="y_initial_pos")
        
        if traj_type == 'Brownian Motion':
            bm_speed = st.slider("Velocidad", min_value=0.1, max_value=5.0, value=0.5, key="bm_speed")
            sh.regen_bm_traj(
                [sh.get_svar('x_initial_pos'), sh.get_svar('y_initial_pos')], 
                sh.get_svar('n_steps'),
                sh.get_svar('bm_speed')
            )
        elif traj_type == 'Lévy Flight':
            lf_alpha = st.slider("Exponente Levy (alpha)", min_value=0.1, max_value=2.0, value=0.5, key="lf_alpha")
            lf_beta = st.slider("Exponente simetría (beta)", min_value=-0.99, max_value=0.99, value=0.0, key="lf_beta")
            sh.regen_lf_traj(
                [sh.get_svar('x_initial_pos'), sh.get_svar('y_initial_pos')], 
                sh.get_svar('n_steps'),
                sh.get_svar('lf_alpha'),
                sh.get_svar('lf_beta')
            )
        else:
            crw_exp = st.slider("Velocidad", min_value=0.1, max_value=1.0, value=0.5, key="crw_exp")
            sh.regen_crw_traj(
                [sh.get_svar('x_initial_pos'), sh.get_svar('y_initial_pos')], 
                sh.get_svar('n_steps'),
                sh.get_svar('crw_exp')
            )
        metrics_type = st.radio("Tipo de Métricas", ('Path Length', 'Mean Squared Displacement'), key="metrics_type")
        if metrics_type == 'Path Length':
            sh.regen_traj_pl()
        else:
            sh.regen_traj_msd()

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
        x = sh.get_svar('trajectory_df').x_pos,
        y = sh.get_svar('trajectory_df').y_pos,
        z = sh.get_svar('trajectory_df').index,
        trace_name = 'BM 2D Trajectory'
    )
    st.plotly_chart(fig_traj_3d, use_container_width=True)
with traj_metrics_2d:
    st.subheader("Gráfica de Métricas")
    plots.add_2d_line_trace(
        target=fig_metr_2d,
        x = sh.get_svar('metrics_df').x_pos,
        y = sh.get_svar('metrics_df').y_pos,
        trace_name=f"{sh.get_svar('traj_type')}_{sh.get_svar('metrics_type')}"
    )
    st.plotly_chart(fig_metr_2d, use_container_width=True)