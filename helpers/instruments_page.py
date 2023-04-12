import streamlit as st

from helpers.utils import print_widgets_separator
from helpers.TEI48 import main_data as main_data_T48, main_zero as main_zero_T48, main_fonct as main_fonct_T48
from helpers.TEI49 import main_data as main_data_T49, main_zero as main_zero_T49, main_fonct as main_fonct_T49

def main():
    # ---------------------------- SIDEBAR -------------------------------- #
    print_widgets_separator(1, sidebar=True)

    instruments = st.sidebar.selectbox("Instrument", ['TEI 49', 'TEI 48'])
    data_type = st.sidebar.selectbox("Type de données", ['DATA', 'FONCT', 'ZERO'])

    # ------------------------- PAGE CONTENT ----------------------------- #

    if instruments == 'TEI 48':
        if data_type == 'DATA':
            return  main_data_T48()
        elif data_type == 'FONCT':
            return main_fonct_T48()
        elif data_type == 'ZERO':
            return main_zero_T48()
    elif instruments == 'TEI 49':
        if data_type == 'DATA':
            return main_data_T49()
        elif data_type == 'FONCT':
            return main_fonct_T49()
        elif data_type == 'ZERO':
            return main_zero_T49()