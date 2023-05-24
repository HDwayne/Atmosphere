import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from helpers.utils import df_resample_mean

def data_TEI48():
    if "Pdm_TEI48_Data" in st.session_state["dfs"]:
        TEI48_Data = st.session_state["dfs"]["Pdm_TEI48_Data"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe y.",
            (col for col in TEI48_Data.columns if col != "valid" and col != "20t_Date"),
        )
        fig = px.line(TEI48_Data, x="20t_Date", y=y_data)
        st.plotly_chart(fig, use_container_width=True)

        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Data.describe().loc[["min", "max", "mean", "count"]])

        st.download_button(
            label=f"Télécharger les données moyénnées (pdm_coanalyzer_L2a_CO_{st.session_state.date}_V01.txt)",
            data=df_resample_mean(TEI48_Data, "5T", ["5d_CO"]).to_csv(sep=";"),
            file_name=f"pdm_coanalyzer_L2a_CO_{st.session_state.date}_V01.txt",
            mime="text/plain",
        )
    else:
        st.error(
            "Pdm_TEI49_Data n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )


def zero_TEI48():
    if "Pdm_TEI48_Zero" in st.session_state["dfs"]:
        TEI48_Zero = st.session_state["dfs"]["Pdm_TEI48_Zero"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe x.",
            (
                col
                for col in TEI48_Zero.columns
                if col != "valid"
                and col != "20t_Date"
                and col != "20t_DateZero"
                and col != "20t_DateMaz"
            ),
        )

        if y_data == "5d_moy":
            invalid_datapoints_max(TEI48_Zero["20t_DateZero"], TEI48_Zero[y_data], 20)
        elif y_data == "5.1f_ect":
            invalid_datapoints_max(TEI48_Zero["20t_DateZero"], TEI48_Zero[y_data], 50)
        else:        
            fig = px.line(TEI48_Zero, x="20t_DateZero", y=y_data)
            st.plotly_chart(fig, use_container_width=True)

        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Zero.describe().loc[["min", "max", "mean", "count"]])
    else:
        st.error(
            "Pdm_TEI49_Zero n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )


def fonct_TEI48():
    if "Pdm_TEI48_Fonct" in st.session_state["dfs"]:
        TEI48_Fonct = st.session_state["dfs"]["Pdm_TEI48_Fonct"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe x.",
            (
                col
                for col in TEI48_Fonct.columns
                if col != "valid" and col != "20t_Date"
            ),
        )
        
        if y_data == "6.4f_ratio":
            invalid_datapoints_minmax(TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], 1.1, 1.2)
        elif y_data == "6.0f_agci":
            invalid_datapoints_minmax(TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], 190000, 210000)
        elif y_data == "5.2f_flow":
            invalid_datapoints_min(TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], 1)
        elif y_data == "6.1f_biasvoltage":
            invalid_datapoints_minmax(TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], -110, -120)
        else:        
            fig = px.line(TEI48_Fonct, x="20t_Date", y=y_data)
            st.plotly_chart(fig, use_container_width=True)        
        
        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Fonct.describe().loc[["min", "max", "mean", "count"]])
    else:
        st.error(
            "Pdm_TEI49_Fonct n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )

        """
        fig, ax = plt.subplots()
        ax.plot(TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data])
        ax.set_xlabel("20t_Date")
        ax.set_ylabel(str(y_data))
        
        st.pyplot(fig)
        """
        
def invalid_datapoints_minmax(x, y, min, max):
    # Define the interval and the color for points outside the interval
    interval_min = min
    interval_max = max
    outside_color = 'red'

    # Create a list to store the colors of each data point
    colors = []

    # Iterate over the data points and assign colors based on the interval
    for xi, yi in zip(x, y):
        if yi < interval_min or yi > interval_max:
            colors.append(outside_color)
        else:
            colors.append('blue')  # Default color for points inside the interval

    # Create the line chart
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers', marker=dict(color=colors)))

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

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

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)