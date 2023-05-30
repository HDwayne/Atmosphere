import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from helpers.utils import df_resample_mean, export_yaml_file
from helpers.filter import *


def slide_change_zero(y_data):
    value = st.session_state[f"slider_{y_data}"]
    st.session_state["yaml"]["Pdm_TEI48_Zero"][y_data]["max"] = value


def slide_change_fonct_minmax(y_data):
    value = st.session_state[f"slider_{y_data}"]
    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["min"] = value[0]
    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["max"] = value[1]


def slide_change_fonct_min(y_data):
    value = st.session_state[f"slider_{y_data}"]
    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["min"] = value


def apply_filter(df_smooth):
    st.session_state["dfs"]["Pdm_TEI48_Data"] = df_smooth


def generate_data():
    maindata = df_resample_mean(
        st.session_state["dfs"]["Pdm_TEI48_Data"], "5T", ["5d_CO"]
    )
    fonctdata = df_resample_mean(st.session_state["dfs"]["Pdm_TEI48_Fonct"], "5T")
    zerodata = df_resample_mean(
        st.session_state["dfs"]["Pdm_TEI48_Zero"], "5T", time_col="20t_DateZero"
    )

    #with st.expander("NEED HELP", expanded=False):
    #    st.write(maindata, fonctdata, zerodata)

    return maindata.to_csv(sep=";")


def data_TEI48():
    if "Pdm_TEI48_Data" in st.session_state["dfs"]:
        TEI48_Data = st.session_state["dfs"]["Pdm_TEI48_Data"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe y.",
            (col for col in TEI48_Data.columns if col != "valid" and col != "20t_Date"),
        )
        fig = px.line(TEI48_Data, x="20t_Date", y=y_data)
        st.plotly_chart(fig, use_container_width=True)

        if st.button("Appliquer le filtre ebarbeur", key="48"):
                
            smooth_df = trimming_filter(TEI48_Data, str(y_data), 5, 50)

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
                    x=TEI48_Data["20t_Date"],
                    y=TEI48_Data[y_data],
                    mode="lines",
                    name="Données originales",
                    line=dict(color="pink"),
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            st.button(
                "save", key="48applyebarbeur", on_click=apply_filter, args=(smooth_df,)
            )

        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Data.describe().loc[["min", "max", "mean", "count"]])

        st.download_button(
            label=f"Télécharger les données moyénnées (pdm_coanalyzer_L2a_CO_{st.session_state.date}_V01.txt)",
            data=generate_data(),
            file_name=f"pdm_coanalyzer_L2a_CO_{st.session_state.date}_V01.txt",
            mime="text/plain",
        )
    else:
        st.error(
            "Pdm_TEI49_Data n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )


def fonct_TEI48():
    if "Pdm_TEI48_Fonct" in st.session_state["dfs"]:
        TEI48_Fonct = st.session_state["dfs"]["Pdm_TEI48_Fonct"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe y.",
            (
                col
                for col in TEI48_Fonct.columns
                if col != "valid" and col != "20t_Date"
            ),
        )

        if y_data == "6.4f_ratio":
            values = st.slider(
                "Choisissez une intervalle costumisée 👇",
                1.1,
                1.2,
                (
                    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["min"],
                    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["max"],
                ),
                step=0.0001,
                on_change=slide_change_fonct_minmax,
                args=(y_data,),
                key=f"slider_{y_data}",
            )
            invalid_datapoints_minmax(
                TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], values[0], values[1]
            )

        elif y_data == "6.0f_agci":
            values = st.slider(
                "Choisissez une intervalle costumisée 👇",
                190000,
                210000,
                (
                    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["min"],
                    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["max"],
                ),
                step=100,
                on_change=slide_change_fonct_minmax,
                args=(y_data,),
                key=f"slider_{y_data}",
            )
            invalid_datapoints_minmax(
                TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], values[0], values[1]
            )

        elif y_data == "6.1f_biasvoltage":
            values = st.slider(
                "Choisissez une intervalle costumisée 👇",
                -110.0,
                -120.0,
                (
                    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["min"],
                    st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["max"],
                ),
                step=0.001,
                on_change=slide_change_fonct_minmax,
                args=(y_data,),
                key=f"slider_{y_data}",
            )
            invalid_datapoints_minmax(
                TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], values[0], values[1]
            )
        elif y_data == "5.2f_flow":
            value = st.slider(
                "Choisissez une intervalle costumisée 👇",
                1.0,
                10.0,
                st.session_state["yaml"]["Pdm_TEI48_Fonct"][y_data]["min"],
                on_change=slide_change_fonct_min,
                args=(y_data,),
                key=f"slider_{y_data}",
            )
            invalid_datapoints_min(TEI48_Fonct["20t_Date"], TEI48_Fonct[y_data], value)
        else:
            fig = px.line(TEI48_Fonct, x="20t_Date", y=y_data)
            st.plotly_chart(fig, use_container_width=True)

        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Fonct.describe().loc[["min", "max", "mean", "count"]])

        st.download_button(
            label="Télécharger les paramètres de fonctionnement (yaml)",
            data=export_yaml_file(st.session_state["yaml"]),
            file_name="config.yaml",
            key="YAML48F",
        )

    else:
        st.error(
            "Pdm_TEI49_Fonct n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )


def zero_TEI48():
    if "Pdm_TEI48_Zero" in st.session_state["dfs"]:
        TEI48_Zero = st.session_state["dfs"]["Pdm_TEI48_Zero"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe y.",
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
            values = st.slider(
                "Choisissez une valeur maximum costumisée 👇",
                -20,
                20,
                st.session_state["yaml"]["Pdm_TEI48_Zero"][y_data]["max"],
                on_change=slide_change_zero,
                args=(y_data,),
                key=f"slider_{y_data}",
            )
            invalid_datapoints_max(
                TEI48_Zero["20t_DateZero"], TEI48_Zero[y_data], values
            )
        elif y_data == "5.1f_ect":
            values = st.slider(
                "Choisissez une valeur maximum costumisée 👇",
                -10,
                50,
                st.session_state["yaml"]["Pdm_TEI48_Zero"][y_data]["max"],
                on_change=slide_change_zero,
                args=(y_data,),
                key=f"slider_{y_data}",
            )
            invalid_datapoints_max(
                TEI48_Zero["20t_DateZero"], TEI48_Zero[y_data], values
            )
        else:
            fig = px.line(TEI48_Zero, x="20t_DateZero", y=y_data)
            st.plotly_chart(fig, use_container_width=True)

        st.write("Statistiques sur les données brutes")
        st.write(TEI48_Zero.describe().loc[["min", "max", "mean", "count"]])

        st.download_button(
            label="Télécharger les paramètres de fonctionnement (yaml)",
            data=export_yaml_file(st.session_state["yaml"]),
            file_name="config.yaml",
            key="YAML48Z",
        )
    else:
        st.error(
            "Pdm_TEI48_Zero n'est pas dans la session. Merci de charger une archive contenant les données nécessaires."
        )
