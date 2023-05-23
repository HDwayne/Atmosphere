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
    generate_zip,
    load_yaml_file,
)
from helpers.TEI48 import *
from helpers.TEI49 import *


def home():
    # Sidebar

    with st.sidebar:
        st.markdown(
            show_Laero_logo(100, [1, 1, 1, 1], margin=[0, 0, 0, 0]),
            unsafe_allow_html=True,
        )

        print_widgets_separator(sidebar=True)

        with st.form("my-form", clear_on_submit=True):
            file = st.file_uploader(
                "Veuillez choisir un fichier", accept_multiple_files=False, type=["zip"]
            )
            yaml_file = st.file_uploader("Upload YAML File", type=["yaml", "yml"])
            st.form_submit_button("submit")

        if yaml_file is not None:
            data = load_yaml_file(yaml_file)
            st.session_state["yaml"] = data

    # Main page

    if file is None:
        st.header("Outils de visualisation des données météorologiques et chimiques")

        st.write(
            "Cet outil permet de visualiser les données provenant d'un analyseur d'ozone et d'un analyseur de monoxyde de carbone (sous forme graphique)."
        )
        st.write(
            "👈 Commencez par choisir l'origine de données, et puis soit mettez en ligne un fichier local, soit saisissez l'adresse du serveur distant !"
        )
    else:
        if not CheckZipFileName(file.name):
            st.sidebar.error("Le nom du fichier ne respecte pas la syntaxe")
        else:
            # remove file from session state if exist
            delete_session_state_rule(checkFileName)

            # add file to session state
            added_file = dfs_to_session_state(read_zip_file(file))

            st.sidebar.success(
                f'Les fichiers suivants ont été ajoutés : {", ".join(added_file)}'
            )

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

            download_data = st.download_button(
                label="Télecharger les données",
                data=generate_zip(
                    st.session_state["dfs"]["Pdm_TEI48_Data"], "Pdm_TEI48_Data"
                ),
                file_name="data.zip",
                mime="application/zip",
            )
            if download_data:
                st.success("Fichier télechargé !", icon="✅")

            download_yaml = st.download_button(
                label="Telecharger les paramètres de configuration de l'outil",
                data=generate_zip(st.session_state["yaml"], "yaml"),
                file_name="config.zip",
                mime="",
            )
            if download_yaml:
                st.write("Fichier téléchargé.")

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
