import streamlit as st
from helpers.filter import *


def data_TEI49():
    if "Pdm_TEI49_Data" in st.session_state["dfs"]:
        TEI49_Data = st.session_state["dfs"]["Pdm_TEI49_Data"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe x.",
            (col for col in TEI49_Data.columns if col != "valid" and col != "20t_Date"),
        )
        st.line_chart(TEI49_Data, x="20t_Date", y=y_data)
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
        st.line_chart(TEI49_Fonct, x="20t_Date", y=y_data)
        st.write("Statistiques sur les données brutes")
        st.write(TEI49_Fonct.describe().loc[["min", "max", "mean", "count"]])
    else:
        st.error(
            "Pdm_TEI49_Data n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )


def filter_TEI49():
    st.title("Filtres sur les données de fonctionnement")

    filters_widgets(st.session_state["dfs"]["Pdm_TEI49_Fonct"], "Pdm_TEI49_Fonct")
