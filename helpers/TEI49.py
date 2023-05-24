import streamlit as st
from helpers.utils import df_resample_mean
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

def filtre_ebarbeur(df : pd.DataFrame, type_donnees : str, val_manq : int, track_bar_coupure : int, track_bar_nbre_pts : int, track_bar_ebarbage : int) -> pd.DataFrame:
    """
    Applies a trimming filter to a dataframe. 
    It basically replaces the lowest value with one that is slightly higher and the highest value with one that is slightly lower until the curve of the graph is smooth

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to filter.
    type_donnees : 
        Name of the column to filter 
    val_manq : int
        An int representing invalid data (-999 for ex)
    track_bar_coupure : int
        The chosen time interval for the sliding window 
    track_bar_nbre_pts : int
        A number of points (idk?)
    track_bar_ebarbage : int
        The number of points that need to get fixed

    Returns
    -------
    pd.DataFrame
        The filtered dataframe (copy).
    """
    filtered_df = df.copy()
    nb_data = len(df)
    nb_pts = 0
    i_deb = 0
    is_calcul = False
    coupure = datetime.datetime.combine(datetime.date.today(), datetime.time.min) + datetime.timedelta(minutes=track_bar_coupure)
    coupure = coupure - datetime.datetime.combine(datetime.date.today(), datetime.time.min)

    # tableau pour stocker des données intermédiaires
    stat = []

    date = filtered_df.iloc[0]['20t_Date']

    #timestamp = datetime.datetime.timestamp(time_part)

    # Convert Timestamp to float representation
    date_float = date.timestamp()

    for jj in range(1, nb_data-1):
        if filtered_df.iloc[jj][type_donnees] > val_manq:
            # ici on filtre pour ne pas prendre en compte les valeurs manquantes style -999.
            # Vous filtrez pour prendre juste des valeurs positives
            if filtered_df.iloc[jj]['20t_Date'] - pd.Timestamp.fromtimestamp(date_float) < coupure:
                # On stocke les données sur un intervalle de temps
                stat.append(filtered_df.iloc[jj][type_donnees]) # data[jj].valTmp = concentration en O3 ou en CO
            else:
                is_calcul = True

            date = filtered_df.iloc[jj]['20t_Date']

        # TrackBarNbrePts->Position : critère de filtrage ou nom selon un nombre de point
        if jj - i_deb >= track_bar_nbre_pts:
            is_calcul = True

        # Recalcul
        if is_calcul:
            stat.sort()
            nb_pts = min(track_bar_ebarbage, len(stat)-1)

            if nb_pts > (len(stat) - 1) // 2:
                nb_pts = (len(stat) - 1) // 2

            if nb_pts >= 0:
                filtre_min = stat[nb_pts - 1]
                filtre_max = stat[len(stat)- nb_pts - 1]

            else:
                filtre_min = -1000000.0
                filtre_max = 1000000.0

            for ii in range(i_deb, jj):
                if ii < len(filtered_df) and filtered_df.iloc[ii][type_donnees] > val_manq:
                    if filtered_df.iloc[ii][type_donnees] < filtre_min:
                        #ajouter une colonne au dataframe pour stocker les valeurs à filtrer ou recopier le df avant d'appliquer le filtre
                        filtered_df.at[ii,type_donnees] = filtre_min 
                    elif filtered_df.iloc[ii][type_donnees] > filtre_max:
                        filtered_df.at[ii,type_donnees]  = filtre_max
                    else:
                        filtered_df.at[ii,type_donnees] = df.iloc[ii][type_donnees]
                else :
                     if ii < len(filtered_df):
                        filtered_df.at[ii,type_donnees]  = df.iloc[ii][type_donnees]

            i_deb = jj
            is_calcul = False
            stat.clear()
    return filtered_df

def data_TEI49():
    if "Pdm_TEI49_Data" in st.session_state["dfs"]:
        TEI49_Data = st.session_state["dfs"]["Pdm_TEI49_Data"]

        y_data = st.selectbox(
            "Veuillez choisir les données pour l'axe x.",
            (col for col in TEI49_Data.columns if col != "valid" and col != "20t_Date"),
        )

        fig = px.line(TEI49_Data, x="20t_Date", y=y_data)
        st.plotly_chart(fig, use_container_width=True)

        TEI49_Data_Filtre = TEI49_Data.copy()
        if st.button('filtre ebarbeur'):
            TEI49_Data_Filtre = filtre_ebarbeur(TEI49_Data, str(y_data), -999, 5, 10, 1)

            fig = px.line(TEI49_Data_Filtre, x="20t_Date", y=y_data, color_discrete_sequence=['teal'], labels="Données filtrées ("+str(y_data)+")")
            fig.update_traces(showlegend=True)

            fig.add_trace(go.Scatter(x=TEI49_Data["20t_Date"], y=TEI49_Data[y_data], mode='lines', name='Données originales', line=dict(color='blue')))
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