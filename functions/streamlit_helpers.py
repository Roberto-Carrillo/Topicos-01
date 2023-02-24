import streamlit as st
from functions import streamlit_helpers as sh
from functions import trajectories as tr
from functions import metrics as mt

def load_text(file_path):
    """A convenience function for reading in the files used for the site's text"""
    with open(file_path) as in_file:
        return in_file.read()

def get_svar(name):
    return st.session_state[name]

def regen_bm_traj(start_pos, n_steps, speed):
    st.session_state.trajectory_df = tr.create_brownian_trajectory(start_pos, n_steps, speed)

def regen_lf_traj(start_pos, n_steps, alpha, beta):
    st.session_state.trajectory_df = tr.create_levy_trajectory(start_pos, n_steps, alpha, beta)

def regen_crw_traj(start_pos, n_steps, crw_exp):
    st.session_state.trajectory_df = tr.create_crw_trajectory(start_pos, n_steps, crw_exp)

def regen_traj_pl():
    st.session_state.metrics_df = mt.create_traj_pl(get_svar('trajectory_df'))

def regen_traj_msd():
    st.session_state.metrics_df = mt.create_traj_msd(get_svar('trajectory_df'))


__all__ = ["load_text", "get_svar", "regen_bm_traj", "regen_lf_traj", "regen_crw_traj", "regen_traj_pl", "regen_traj_msd"]