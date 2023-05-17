import streamlit as st
from helpers.utils import *
from helpers.TEI48 import *
from helpers.TEI49 import main_data , main_zero as main_zero_T49, main_fonct as main_fonct_T49, main_data_new as data_T49, main_fonct_new as fonct_T49
from helpers.utils import convert_df, generate_zip

def main():
    st.set_page_config(
        page_title="BE",
        layout="wide",
        initial_sidebar_state="auto"
    )

    with st.sidebar:
        html_code = show_Laero_logo(100, [1, 1, 1, 1], margin=[0, 0, 0, 0])
        st.markdown(html_code, unsafe_allow_html=True)

        print_widgets_separator(sidebar=True)

        choice = st.radio(
            "📊 Sélectionnez la source de données",
            ("📁 Fichier local", "📥 Serveur distant")
        )
        if choice == "📁 Fichier local":
            file = st.file_uploader("Veuillez choisir un fichier",
                                    accept_multiple_files=False,
                                    type=['zip'])
        elif choice == "📥 Serveur distant":
            site = st.text_input("Saisissez l'adresse du serveur 👇")
    
    if file is None:
        st.header('Outils de visualisation des données météorologiques et chimiques')

        st.write("Cet outil permet de visualiser les données provenant d'un analyseur d'ozone et d'un analyseur de monoxyde de carbone (sous forme graphique).")
        st.write("👈 Commencez par choisir l'origine de données, et puis soit mettez en ligne un fichier local, soit saisissez l'adresse du serveur distant !")

    if choice == "📁 Fichier local" and file is not None:
        if not CheckZipFileName(file.name):
            st.sidebar.error('Le nom du fichier ne respecte pas la syntaxe')
        else:
            # remove file from session state
            delete_session_state_rule(checkFileName)

            # add file to session state
            added_file = []
            dfs = read_zip_file(file)
            apply_time_dfs(dfs, ['20t_Date'], "%d/%m/%Y,%H:%M:%S")
            for key, value in dfs.items():
                added_file.append(key)
                if not key in st.session_state:
                    st.session_state[key] = value
                else:
                    st.session_state[key] = st.session_state[key]
                    # Iterate over the columns in the DataFrame
                for col in value.columns:
                    # Check if the column name contains "\r"
                    if '\r' in col:
                        # Clean the column name by removing "\r"
                        new_col = col.replace('\r', '')
                        # Rename the column in the DataFrame
                        value.rename(columns={col: new_col}, inplace=True)


            # display page
            st.sidebar.success(f'Les fichiers suivants ont été ajoutés : {", ".join(added_file)}')

            # Donnees enregistreees - donnees brutes etaient ici
            
            tei48, tei49 = st.tabs(["TEI 48", "TEI 49"])
            
            with tei48:
                DATA, FONCT, ZERO = st.tabs(["Données principales", "Fonctionnement", "Zéro"])
                with DATA:
                    data_TEI48()
                with FONCT:
                    fonct_TEI48()
                with ZERO:
                    zero_TEI48()
            
            with tei49:
                DATA, FONCT, ZERO = st.tabs(["Données principales", "Fonctionnement", "Zéro"])
                with DATA:
                    data_T49()
                with FONCT:
                    fonct_T49()
                with ZERO:
                    main_zero_T49()
          
            download_data = st.download_button(
                label="Télecharger les données", 
                data=generate_zip(st.session_state.Pdm_TEI48_Data, "Pdm_TEI48_Data"),
                file_name="data.zip", 
                mime="application/zip",
                key=67
                )
            if download_data:
                st.success('Fichier télechargé !', icon="✅")


            b2 = st.button("Telecharger les paramètres de configuration de l\'outil", key="4")
            if b2:
                st.write('Fichier téléchargé.')

            #st.subheader('Données enregistrées: ')
            with st.expander("Cliquez ici pour consulter les données brutes 👋"):
                number_file = getNumberFileImpoted()
                if number_file == 0:
                    st.info('Aucune donnée enregistré, veuillez importer un fichier zip depuis la section de gauche.')
                elif number_file != 5:
                    st.warning('Le fichier zip utilisé ne contient pas le nombre de fichiers attendus. certaines fonctionnalités sont susceptibles de ne pas fonctionner correctement.')
                
                for key, value in st.session_state.items():
                    if checkFileName(key, contain_date=False):
                        st.write(key, value)


if __name__ == '__main__':
    main()