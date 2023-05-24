import streamlit as st
from helpers.utils import df_resample_mean
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
from helpers.filter import filtre_ebarbeur

#variables globales
iter = 0
smooth_df = pd.DataFrame()


def data_TEI49():
    if "Pdm_TEI49_Data" in st.session_state["dfs"]:
        TEI49_Data = st.session_state["dfs"]["Pdm_TEI49_Data"]
        
        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe x.",
            (col for col in TEI49_Data.columns if col != "valid" and col != "20t_Date"),
        )

        fig = px.line(TEI49_Data, x="20t_Date", y=y_data)
        st.plotly_chart(fig, use_container_width=True)

        #bouton filtre ebarbeur
        global iter #nb d'itérations
        global smooth_df #df filtrée

        if st.button('filtre ebarbeur', key = "49"):
            if iter == 0 :
                smooth_df = filtre_ebarbeur(TEI49_Data, str(y_data), -999, 5, 6, 8000)
            else :
                smooth_df = filtre_ebarbeur(smooth_df, str(y_data), -999, 5, 6, 8000)

            iter += 1
            fig = px.line(smooth_df, x="20t_Date", y=y_data, color_discrete_sequence=['teal'], labels="Données filtrées ("+str(y_data)+")")
            fig.update_traces(showlegend=True)

            fig.add_trace(go.Scatter(x=TEI49_Data["20t_Date"], y=TEI49_Data[y_data], mode='lines', name='Données originales', line=dict(color='pink')))
            st.plotly_chart(fig, use_container_width=True)
            
        st.write("Statistiques sur les données brutes")
        st.write(TEI49_Data.describe().loc[["min", "max", "mean", "count"]])                

        st.download_button(
            label=f"Télécharger les données moyénnées (pdm_o3analyzer_L2a_O3_{st.session_state.date}_V01.txt)",
            data=df_resample_mean(TEI49_Data, "5T", ["4d_Pression"]).to_csv(sep=";"),
            file_name=f"pdm_o3analyzer_L2a_O3_{st.session_state.date}_V01.txt",
            mime="text/plain",
        )
    else:
        st.error(
            "Pdm_TEI49_Data n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )


def fonct_TEI49():
    if "Pdm_TEI49_Fonct" in st.session_state["dfs"]:
        TEI49_Fonct = st.session_state["dfs"]["Pdm_TEI49_Fonct"]
        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe x.",
            (
                col
                for col in TEI49_Fonct.columns
                if col != "valid" and col != "20t_Date"
            ),
        )

        if y_data == "4.2f_flowA":
            value = st.slider('Vous pouvez modifier la valeur minimum en glissant la barre ci-dessous 👇', 1.0, 100.0, 1.0, step=0.01)
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], value)
        elif y_data == "4.2f_flowB":
            value = st.slider('Vous pouvez modifier la valeur minimum en glissant la barre ci-dessous 👇', 1.0, 100.0, 1.0, step=0.01)
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], value)
        elif y_data == "6d_cellAInt":
            value = st.slider('Vous pouvez modifier la valeur minimum en glissant la barre ci-dessous 👇', 80000, 1000000, 80000)
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], value)
        elif y_data == "6d_cellBInt":
            value = st.slider('Vous pouvez modifier la valeur minimum en glissant la barre ci-dessous 👇', 80000, 1000000, 80000)
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], value)
        else:
            fig = px.line(TEI49_Fonct, x="20t_Date", y=y_data)
            st.plotly_chart(fig, use_container_width=True)

        st.write("Statistiques sur les données brutes")
        st.write(TEI49_Fonct.describe().loc[["min", "max", "mean", "count"]])
    else:
        st.error(
            "Pdm_TEI49_Data n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )

def invalid_datapoints_min(x, y, min):
    # Define the interval and the color for points outside the interval
    interval_min = min
    outside_color = 'red'

    # Create a list to store the colors of each data point
    colors = []

    # Iterate over the data points and assign colors based on the interval
    for xi, yi in zip(x, y):
        if yi < interval_min:
            colors.append(outside_color)
        else:
            colors.append('blue')  # Default color for points inside the interval

    # Create the line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers', marker=dict(color=colors)))

    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='blue'), name='Valide'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='red'), name='Non-valide'))

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def invalid_datapoints_max(x, y, max):
    # Define the interval and the color for points outside the interval
    interval_max = max
    outside_color = 'red'

    # Create a list to store the colors of each data point
    colors = []

    # Iterate over the data points and assign colors based on the interval
    for xi, yi in zip(x, y):
        if yi > interval_max:
            colors.append(outside_color)
        else:
            colors.append('blue')  # Default color for points inside the interval

    # Create the line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers', marker=dict(color=colors)))

    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='blue'), name='Valide'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='red'), name='Non-valide'))

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)