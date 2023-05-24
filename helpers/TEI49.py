import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def data_TEI49():
    if "Pdm_TEI49_Data" in st.session_state["dfs"]:
        TEI49_Data = st.session_state["dfs"]["Pdm_TEI49_Data"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe x.",
            (col for col in TEI49_Data.columns if col != "valid" and col != "20t_Date"),
        )

        fig = px.line(TEI49_Data, x="20t_Date", y=y_data)
        st.plotly_chart(fig, use_container_width=True)

        st.write("Statistiques sur les données brutes")
        st.write(TEI49_Data.describe().loc[["min", "max", "mean", "count"]])        
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
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], 1)
        elif y_data == "4.2f_flowB":
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], 1)
        elif y_data == "6d_cellAInt":
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], 80000)
        elif y_data == "6d_cellBInt":
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], 80000)
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