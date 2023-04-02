import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from helpers.filter import filter_dataframe
from helpers.utils import print_widgets_separator

XAXIS=dict(
    rangeselector=dict(
        buttons=list([
            dict(count=1,
                label="1h",
                step="hour",
                stepmode="todate"),
            dict(count=5,
                label="5h",
                step="hour",
                stepmode="todate"),
            dict(count=10,
                label="10h",
                step="hour",
                stepmode="todate"),
            dict(count=1,
                label="Tout",
                step="all")
        ])
    ),
    rangeslider=dict(
        visible=True
    ),
    type="date",
)

YAXYS=dict(
    side="right",
)

def main_data():
    st.header('TEI 49 Data')

    if 'Pdm_TEI49_Data' in st.session_state:
        Pdm_TEI49_Data = filter_dataframe(st.session_state.Pdm_TEI49_Data, "Pdm_TEI49_Data_filter")

        print_widgets_separator()

        left, right = st.columns((1, 1))
        left.write('Statistiques sur les données brutes')
        left.write(Pdm_TEI49_Data.describe().loc[['min', 'max', 'mean', 'count']])
        right.write('Statistiques sur les données filtrées')
        right.write(Pdm_TEI49_Data[Pdm_TEI49_Data['valid'] == True].describe().loc[['min', 'max', 'mean', 'count']])

        # TODO: Color blue if valid, red if not (soould'nt depend on the size of the dataset)

        if 'valid' not in Pdm_TEI49_Data.columns:
            fig_ozone= px.line(data_frame=Pdm_TEI49_Data, x='20t_Date', y='4d_Ozone')
            fig_pression= px.line(data_frame=Pdm_TEI49_Data, x='20t_Date', y='4d_Pression')
        else:
            fig_ozone = px.line(data_frame=Pdm_TEI49_Data, x='20t_Date', y='4d_Ozone', color='valid', markers=True, color_discrete_sequence=['blue', 'red'])
            fig_pression = px.line(data_frame=Pdm_TEI49_Data, x='20t_Date', y='4d_Pression', color='valid', markers=True, color_discrete_sequence=['blue', 'red'])
        
        fig_ozone.update_layout(title_text="Mesure d'Ozone")
        fig_ozone.update_layout(xaxis=XAXIS)
        st.plotly_chart(fig_ozone, use_container_width=True)

        fig_pression.update_layout(title_text="Mesure de Pression")
        fig_pression.update_layout(xaxis=XAXIS)
        st.plotly_chart(fig_pression, use_container_width=True)

        if 'Pdm_TEI49_Data_filter' in st.session_state:
            st.subheader('Filtre appliqué (Debug)')
            st.write(st.session_state["Pdm_TEI49_Data_filter"])
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

        fig_flow = go.Figure()
        fig_flow.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['4.2f_flowA'], name='4.2f_flowA'))
        fig_flow.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['4.2f_flowB'], name='4.2f_flowB'))
        fig_flow.update_layout(title_text="Mesure de débit d'air des cellules A et B")
        fig_flow.update_layout(xaxis=XAXIS, yaxis=YAXYS)
        st.plotly_chart(fig_flow, use_container_width=True)

        fig_bkg = go.Figure()
        fig_bkg.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['3.1f_bkg'], name='3.1f_bkg'))
        fig_bkg.update_layout(title_text="Mesure de fond")
        fig_bkg.update_layout(xaxis=XAXIS, yaxis=YAXYS)
        st.plotly_chart(fig_bkg, use_container_width=True)

        fig_coef = go.Figure()
        fig_coef.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['5.2f_coef'], name='5.2f_coef'))
        fig_coef.update_layout(title_text="Mesure de coefficient")
        fig_coef.update_layout(xaxis=XAXIS, yaxis=YAXYS)
        st.plotly_chart(fig_coef, use_container_width=True)

        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['5.1f_benchT'], name='5.1f_benchT'))
        fig_temp.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['5.1f_O3lampT'], name='5.1f_O3lampT'))
        fig_temp.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['5.1f_intT'], name='5.1f_intT'))
        fig_temp.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['5.1f_lampSetting'], name='5.1f_lampSetting'))
        fig_temp.update_layout(title_text="Mesure de température")
        fig_temp.update_layout(xaxis=XAXIS, yaxis=YAXYS)
        st.plotly_chart(fig_temp, use_container_width=True)

        fig_cell = go.Figure()
        fig_cell.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['6d_cellAInt'], name='6d_cellAInt'))
        fig_cell.add_trace(go.Scatter(x=Pdm_TEI49_Fonct['20t_Date'], y=Pdm_TEI49_Fonct['6d_cellBInt'], name='6d_cellBInt'))
        fig_cell.update_layout(title_text="Mesure d'intensité des cellules A et B")
        fig_cell.update_layout(xaxis=XAXIS, yaxis=YAXYS)
        st.plotly_chart(fig_cell, use_container_width=True)
    else:
        st.error('Pdm_TEI49_Fonct n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')