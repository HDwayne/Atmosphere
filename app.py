import streamlit as st
from helpers.home import home 

if __name__ == '__main__':
    st.set_page_config(
        page_title="ATMOSPHERE",
        layout="wide",
        initial_sidebar_state="auto",
        page_icon="assets/finalicon.png"
    ) 
    home()