import streamlit as st

from helpers.utils import print_widgets_separator

def main():
    # ---------------------------- SIDEBAR -------------------------------- #
    print_widgets_separator(1, sidebar=True)

    instruments = st.sidebar.selectbox("Instrument", ['TEI 48', 'TEI 49'])
    data_type = st.sidebar.selectbox("Type de données", ['DATA', 'FONCT', 'ZERO'])

    # ------------------------- PAGE CONTENT ----------------------------- #

    if instruments == 'TEI 48':
        if data_type == 'DATA':
            st.title('TEI 48 Data')
        elif data_type == 'FONCT':
            st.title('TEI 48 Fonct')
        elif data_type == 'ZERO':
            st.title('TEI 48 Zero')
    elif instruments == 'TEI 49':
        if data_type == 'DATA':
            st.title('TEI 49 Data')
        elif data_type == 'FONCT':
            st.title('TEI 49 Fonct')
        elif data_type == 'ZERO':
            st.title('TEI 49 Zero')