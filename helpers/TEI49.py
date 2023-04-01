import streamlit as st
import plotly.express as px

def main_data():
    st.header('TEI 49 Data')

    if 'Pdm_TEI49_Data' in st.session_state:
        Pdm_TEI49_Data = st.session_state.Pdm_TEI49_Data

        st.write(Pdm_TEI49_Data.describe().loc[['min', 'max', 'mean']])
        
        st.subheader('Mesure Ozone')

        fig_ozone = px.line(Pdm_TEI49_Data, x='20t_Date', y='4d_Ozone')
        st.plotly_chart(fig_ozone, use_container_width=True)
        
        st.subheader('Mesure de Pression')
        
        fig_pression = px.line(Pdm_TEI49_Data, x='20t_Date', y='4d_Pression')
        st.plotly_chart(fig_pression, use_container_width=True)
    else:
        st.error('Pdm_TEI49_Data n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')

def main_zero():
    st.title('TEI 49 Zero')

    st.info('Cet instrument ne fournit pas de données de zéro.')
          

def main_fonct():
    st.header('TEI 49 Fonct')

    if 'Pdm_TEI49_Fonct' in st.session_state:
        Pdm_TEI49_Fonct = st.session_state.Pdm_TEI49_Fonct
        st.write(Pdm_TEI49_Fonct.describe().loc[['min', 'max', 'mean']])

        st.subheader('4.2f_flowA et 4.2f_flowB')

        fig_flow = px.line(Pdm_TEI49_Fonct, x='20t_Date', y=['4.2f_flowA', '4.2f_flowB'])
        st.plotly_chart(fig_flow, use_container_width=True)

        st.subheader('3.1f_bkg')

        fig_bkg = px.line(Pdm_TEI49_Fonct, x='20t_Date', y='3.1f_bkg')
        st.plotly_chart(fig_bkg, use_container_width=True)

        st.subheader('5.2f_coef')

        fig_coef = px.line(Pdm_TEI49_Fonct, x='20t_Date', y='5.2f_coef')
        st.plotly_chart(fig_coef, use_container_width=True)

        st.subheader('5.1f_benchT, 5.1f_O3lampT, 5.1f_intT, et 5.1f_lampSetting')

        fig_temp = px.line(Pdm_TEI49_Fonct, x='20t_Date', y=['5.1f_benchT', '5.1f_O3lampT', '5.1f_intT', '5.1f_lampSetting'])
        st.plotly_chart(fig_temp, use_container_width=True)

        st.subheader('6d_cellAInt et 6d_cellBInt')

        fig_cell = px.line(Pdm_TEI49_Fonct, x='20t_Date', y=['6d_cellAInt', '6d_cellBInt'])
        st.plotly_chart(fig_cell, use_container_width=True)
    else:
        st.error('Pdm_TEI49_Fonct n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')