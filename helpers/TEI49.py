import streamlit as st
import pandas as pd
import datetime

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
        st.line_chart(TEI49_Data, x="20t_Date", y=y_data)

        if st.button('filtre ebarbeur'):
            TEI49_Data = filtre_ebarbeur(TEI49_Data, y_data, -999, 5, 10, 1)
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
