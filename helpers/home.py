import streamlit as st
from helpers.utils import (
    print_widgets_separator,
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


DEFULT_YAML = {
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
        st.session_state["yaml"] = DEFULT_YAML

    if st.session_state["upload_zip"] is not None:
        zip_file = st.session_state["upload_zip"]
        if not CheckZipFileName(zip_file.name):
            st.sidebar.error("Le nom du fichier ne respecte pas la syntaxe")
        else:
            # remove file from session state if exist
            delete_session_state_rule(checkFileName)

            # add file to session state
            added_file = dfs_to_session_state(read_zip_file(zip_file))

            # save date in session state
            st.session_state["date"] = getDateFromZipFileName(zip_file.name)

            # st.sidebar.success(
            #     f'Les fichiers suivants ont été ajoutés : {", ".join(added_file)}'
            # )


def home():
    # Sidebar

    with st.sidebar:
        st.markdown(
            show_Laero_logo(100, [1, 1, 1, 1], margin=[0, 0, 0, 0]),
            unsafe_allow_html=True,
        )

        print_widgets_separator(sidebar=True)

        with st.form("upload_form", clear_on_submit=True):
            st.file_uploader(
                "Veuillez choisir un fichier",
                accept_multiple_files=False,
                type=["zip"],
                key="upload_zip",
            )
            st.file_uploader(
                "Upload YAML File", type=["yaml", "yml"], key="upload_yaml"
            )
            st.form_submit_button(
                label="submit",
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
                "YAML file is optional, if you don't upload it, default values will be used."
            )

            # download default yaml file
            st.download_button(
                label="Télécharger le template YAML",
                data=export_yaml_file(DEFULT_YAML),
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

        print_widgets_separator()

        # download_yaml = st.download_button(
        #     label="Telecharger les paramètres de configuration de l'outil",
        #     data=generate_zip(st.session_state["yaml"], "yaml"),
        #     file_name="config.zip",
        #     mime="",
        # )
        # if download_yaml:
        #     st.write("Fichier téléchargé.")

        if "yaml" in st.session_state:
            st.write("Paramètres de configuration de l'outil :")
            st.write(st.session_state["yaml"])

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
