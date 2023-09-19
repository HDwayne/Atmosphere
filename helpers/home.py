import streamlit as st
from helpers.utils import (
    show_Laero_logo,
    delete_session_state_rule,
    CheckZipFileName,
    read_zip_file,
    getNumberFileImpoted,
    checkFileName,
    dfs_to_session_state,
    load_yaml_file,
    export_yaml_file,
    getDateFromZipFileName,
)
from helpers.TEI48 import *
from helpers.TEI49 import *


DEFAULT_YAML = {
    "Pdm_TEI49_Fonct": {
        "4.2f_flowA": {"min": 1.0},
        "4.2f_flowB": {"min": 1.0},
        "6d_cellAInt": {"min": 80000},
        "6d_cellBInt": {"min": 80000},
    },
    "Pdm_TEI48_Fonct": {
        "6.4f_ratio": {"min": 1.1, "max": 1.2},
        "6.0f_agci": {"min": 190000, "max": 210000},
        "5.2f_flow": {"min": 1.0},
        "6.1f_biasvoltage": {"min": -110.0, "max": -120.0},
    },
    "Pdm_TEI48_Zero": {
        "5d_moy": {"max": 20},
        "5.1f_ect": {"max": 50},
    },
}


def send_data():
    if st.session_state["upload_yaml"] is not None:
        yaml_file = st.session_state["upload_yaml"]
        data = load_yaml_file(yaml_file)
        st.session_state["yaml"] = data
    else:
        st.session_state["yaml"] = DEFAULT_YAML

    if st.session_state["upload_zip"] is not None:
        zip_file = st.session_state["upload_zip"]
        if not CheckZipFileName(zip_file.name):
            st.sidebar.error("Le nom du fichier ne respecte pas la syntaxe")
        else:
            # remove file from session state if exist
            delete_session_state_rule(checkFileName)

            # add file to session state
            dfs_to_session_state(read_zip_file(zip_file))

            # save date in session state
            st.session_state["date"] = getDateFromZipFileName(zip_file.name)


def home():
    # Sidebar

    with st.sidebar:
        st.markdown(
            show_Laero_logo(100, [1, 1, 1, 1], margin=[0, 0, 0, 0]),
            unsafe_allow_html=True,
        )


        with st.form("upload_form", clear_on_submit=True):
            st.file_uploader(
                "Veuillez choisir un fichier",
                accept_multiple_files=False,
                type=["zip"],
                key="upload_zip",
            )
            st.file_uploader(
                "Déposez le fichier YAML (Optionnel)", type=["yaml", "yml"], key="upload_yaml"
            )
            st.form_submit_button(
                label="Mettre en ligne",
                on_click=send_data,
            )

    # Main page

    if "dfs" not in st.session_state:
        st.header("Outils de visualisation des données météorologiques et chimiques")

        st.write(
            "Cet outil permet de visualiser les données provenant d'un analyseur d'ozone et d'un analyseur de monoxyde de carbone (sous forme graphique)."
        )
        st.write(
            "👈 Commencez par choisir l'origine de données, et puis soit mettez en ligne un fichier local, soit saisissez l'adresse du serveur distant !"
        )

        if "yaml" not in st.session_state:
            st.info(
                "Le fichier YAML est optionnel. En cas de son absence, les valeurs par défaut seront mises."
            )

            # download default yaml file
            if st.button("Préparer le template YAML", key="CYAMLH"):
                st.download_button(
                    label="Télécharger le template YAML",
                    data=export_yaml_file(DEFAULT_YAML),
                    file_name="template.yaml",
                )
    else:
        # display page

        tei48, tei49 = st.tabs(["TEI 48", "TEI 49"])

        with tei48:
            DATA, FONCT, ZERO = st.tabs(
                ["Données principales", "Fonctionnement", "Zéro"]
            )
            with DATA:
                data_TEI48()
            with FONCT:
                fonct_TEI48()
            with ZERO:
                zero_TEI48()

        with tei49:
            DATA, FONCT = st.tabs(["Données principales", "Fonctionnement"])
            with DATA:
                data_TEI49()
            with FONCT:
                fonct_TEI49()

        # commun footer

        with st.expander("Cliquez ici pour consulter les données brutes 👋"):
            number_file = getNumberFileImpoted()
            if number_file == 0:
                st.info(
                    "Aucune donnée enregistré, veuillez importer un fichier zip depuis la section de gauche."
                )
            elif number_file != 5:
                st.warning(
                    "Le fichier zip utilisé ne contient pas le nombre de fichiers attendus. certaines fonctionnalités sont susceptibles de ne pas fonctionner correctement."
                )

            for key, value in st.session_state["dfs"].items():
                if checkFileName(str(key), contain_date=False):
                    st.write(key, value)
