import streamlit as st
from helpers.home import home 

if __name__ == '__main__':
    st.set_page_config(
        page_title="BE",
        layout="wide",
        initial_sidebar_state="auto"
    ) 
    home()