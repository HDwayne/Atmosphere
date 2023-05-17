import pandas as pd
import streamlit as st

def data_TEI48():
    if 'Pdm_TEI48_Data' in st.session_state:
        TEI48_Data = st.session_state.Pdm_TEI48_Data

        y_data = st.selectbox( 
            'Veuillez choisir les données pour l\'axe x.',
            (col for col in TEI48_Data.columns if col != "valid" and col !='20t_Date')
            )
        st.line_chart(TEI48_Data, x='20t_Date', y=y_data)
        st.write('Statistiques sur les données brutes')
        st.write(TEI48_Data.describe().loc[['min', 'max', 'mean', 'count']])
    else:
        st.error('Pdm_TEI49_Data n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')

def zero_TEI48():
    if 'Pdm_TEI48_Zero' in st.session_state:
        TEI48_Zero = st.session_state.Pdm_TEI48_Zero

        y_data = st.selectbox( 
            'Veuillez choisir les données pour l\'axe x.',
            (col for col in TEI48_Zero.columns if col != "valid" and col !='20t_Date' and col !='20t_DateZero' and col !='20t_DateMaz'))
        st.line_chart(TEI48_Zero, x='20t_DateZero', y=y_data)
        st.write('Statistiques sur les données brutes')
        st.write(TEI48_Zero.describe().loc[['min', 'max', 'mean', 'count']])
    else:
        st.error('Pdm_TEI49_Zero n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')

def fonct_TEI48():
    if 'Pdm_TEI48_Fonct' in st.session_state:
        TEI48_Fonct = st.session_state.Pdm_TEI48_Fonct

        y_data = st.selectbox( 
            'Veuillez choisir les données pour l\'axe x.',
            (col for col in TEI48_Fonct.columns if col != "valid" and col !='20t_Date'))
        st.line_chart(TEI48_Fonct, x='20t_Date', y=y_data)
        st.write('Statistiques sur les données brutes')
        st.write(TEI48_Fonct.describe().loc[['min', 'max', 'mean', 'count']])
    else:
        st.error('Pdm_TEI49_Fonct n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')