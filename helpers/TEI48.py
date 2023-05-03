import streamlit as st

def main():
    DATA, FONCT, ZERO = st.tabs(["Données principales", "Fonctionnement", "Zéro"])
    with DATA:
        main_data()
    with FONCT:
        main_fonct()
    with ZERO:
        main_zero()


def main_data():
    st.title('TEI 48 Data')

def main_zero():
    st.title('TEI 48 Zero')

def main_fonct():
    st.title('TEI 48 Fonct')