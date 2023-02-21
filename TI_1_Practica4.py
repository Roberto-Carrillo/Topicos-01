import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard - Tópicos de Industria 1", 
                    page_icon=":chart_with_upwards_trend:",
                    layout="wide",
                    initial_sidebar_state="expanded")

# --- Data Loading ----
# @st.cache
# def get_data():
    

# --- Header Section ----
st.title("Dashboard Caminados aleatorios")
st.subheader("Tópicos de Industria 1 - 2023A")
st.text("Roberto Octavio Carrillo Luevano")

header_left, header_mid, header_right = st.columns([1,2,3], gap="large")
genre = None

# with header_mid:

# Conditional Layout for Selecting Trajectory type
with st.sidebar:
    with st.container():
        st.subheader("Parámetros")
        genre = st.radio("Tipo de Trayectoria", ('Brownian Motion', 'Lévy Flight', 'Correlated Random Walk'))
        steps = st.number_input("Número de pasos", min_value=10, max_value=20000)
        col1, col2 = st.columns(2)

        with col1:
            x_initial_pos = st.number_input("Inicio - X")
        with col2:
            y_initial_pos = st.number_input("Inicio - Y")
        
