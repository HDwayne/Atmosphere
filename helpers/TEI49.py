import streamlit as st
from helpers.utils import df_resample_mean, export_yaml_file
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from helpers.filter import trimming_filter, invalid_datapoints_min


def apply_filter(df_smooth):
    st.session_state["dfs"]["Pdm_TEI49_Data"] = df_smooth


def data_TEI49():
    if "Pdm_TEI49_Data" in st.session_state["dfs"]:
        TEI49_Data = st.session_state["dfs"]["Pdm_TEI49_Data"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe y.",
            (col for col in TEI49_Data.columns if col != "valid" and col != "20t_Date"),
        )

        fig = px.line(TEI49_Data, x="20t_Date", y=y_data)
        st.plotly_chart(fig, use_container_width=True)  

        if st.button("Appliquer le filtre ebarbeur", key="49"):
            smooth_df = trimming_filter(TEI49_Data, str(y_data), 5, 50)
            fig = px.line(
                smooth_df,
                x="20t_Date",
                y=y_data,
                color_discrete_sequence=["teal"],
                labels="Données filtrées (" + str(y_data) + ")",
            )
            fig.update_traces(showlegend=True)

            fig.add_trace(
                go.Scatter(
                    x=TEI49_Data["20t_Date"],
                    y=TEI49_Data[y_data],
                    mode="lines",
                    name="Données originales",
                    line=dict(color="pink"),
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            st.button(
                "save", key="49applyebarbeur", on_click=apply_filter, args=(smooth_df,)
            )

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


def slide_change(y_data):
    value = st.session_state[f"slider_{y_data}"]
    st.session_state["yaml"]["Pdm_TEI49_Fonct"][y_data]["min"] = value


def fonct_TEI49():
    if "Pdm_TEI49_Fonct" in st.session_state["dfs"]:
        TEI49_Fonct = st.session_state["dfs"]["Pdm_TEI49_Fonct"]
        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe y.",
            (
                col
                for col in TEI49_Fonct.columns
                if col != "valid" and col != "20t_Date"
            ),
        )

        if y_data in ["4.2f_flowA", "4.2f_flowB", "6d_cellAInt", "6d_cellBInt"]:
            value = st.slider(
                "Vous pouvez modifier la valeur minimum en glissant la barre ci-dessous 👇",
                1.0 if y_data in ["4.2f_flowA", "4.2f_flowB"] else 80000,
                100.0 if y_data in ["4.2f_flowA", "4.2f_flowB"] else 1000000,
                st.session_state["yaml"]["Pdm_TEI49_Fonct"][y_data]["min"],
                step=0.01 if y_data in ["4.2f_flowA", "4.2f_flowB"] else None,
                on_change=slide_change,
                args=(y_data,),
                key=f"slider_{y_data}",
            )
            invalid_datapoints_min(TEI49_Fonct["20t_Date"], TEI49_Fonct[y_data], value)
        else:
            fig = px.line(TEI49_Fonct, x="20t_Date", y=y_data)
            st.plotly_chart(fig, use_container_width=True)

        st.write("Statistiques sur les données brutes")
        st.write(TEI49_Fonct.describe().loc[["min", "max", "mean", "count"]])

        st.download_button(
            label="Télécharger les paramètres de fonctionnement (yaml)",
            data=export_yaml_file(st.session_state["yaml"]),
            file_name="config.yaml",
            key="YAML49F",
        )
    else:
        st.error(
            "Pdm_TEI49_Data n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )
