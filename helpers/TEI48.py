import streamlit as st
import altair as alt
import pandas as pd
from helpers.utils import df_resample_mean


def data_TEI48():
    if "Pdm_TEI48_Data" in st.session_state["dfs"]:
        TEI48_Data = st.session_state["dfs"]["Pdm_TEI48_Data"]
        st.write(TEI48_Data)

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe y.",
            (col for col in TEI48_Data.columns if col != "valid" and col != "20t_Date"),
        )
        # st.line_chart(TEI48_Data, x="20t_Date", y=y_data)
        c = alt.Chart(TEI48_Data).mark_line().encode(x="20t_Date", y=y_data)
        st.altair_chart(c, use_container_width=True)
        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Data.describe().loc[["min", "max", "mean", "count"]])

        st.download_button(
            label=f"Télécharger les données moyénnées (pdm_coanalyzer_L2a_{st.session_state.date}_V01.txt)",
            data=df_resample_mean(TEI48_Data, "5T", ["5d_CO"]).to_csv(sep=";"),
            file_name=f"pdm_coanalyzer_L2a_{st.session_state.date}_V01.txt",
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
        st.line_chart(TEI48_Zero, x="20t_DateZero", y=y_data)
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
        c = alt.Chart(TEI48_Fonct).mark_line().encode(x="20t_Date", y=y_data)
        st.altair_chart(c, use_container_width=True)
        # st.line_chart(TEI48_Fonct, x="20t_Date", y=y_data)
        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Fonct.describe().loc[["min", "max", "mean", "count"]])
    else:
        st.error(
            "Pdm_TEI49_Fonct n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )
