import streamlit as st


def main():
    st.header('Outils de visualisation des données de l\'analyseur TEI48 et TEI49')
    
    st.write("Développer un outil permettant de visualiser les données sous forme graphique. Ces données proviennent d'un analyseur d'ozone et d'un analyseur de monoxyde de carbone. S'il reste du temps en fin de stage, la gestion d'un instrument de mesure des oxydes d'azote est souhaitable. Plusieurs fichiers sont rattachés à un instrument : Les données proprement dites et les paramètres de fonctionnement de l'instrument : température de fonctionnement, débit des pompes ... Différentes interactions avec l'interface devront permettre d'invalider les données ou de faire des corrections simples, puis de sauvegarder les données validées et moyennées dans un nouveau fichier contenant dans ces métadonnées les informations de corrections. Actuellement les fichiers de données sont au format csv mais une gestion du format NetCdf des donnés finales est à prévoir pour une évolution ultérieure.")
    
    st.subheader('Comment utiliser l\'outil ?')
    
    st.write("L'outil est divisé en deux parties :")
    st.write("1. La partie gauche de l'écran permet de naviguer entre les différentes pages de l'outil.")
    st.write("2. La partie droite de l'écran permet de visualiser les pages et d'interagir avec les données.")
    st.write("Pour utiliser l'outil, il suffit d'importer les fichiers de données depuis l'interface de gauche de la page de données. Il s\'agira ensuite de naviguer sur la page dédié aux instruments puis de sélectionner l'instrument ainsi que le type de données à visualiser. Il sera donc possible de visualiser et d'interagir avec les données depuis leurs pages respectives.")

    st.subheader('Informations utiles')
    
    with st.expander('Format de fichier pris en charge'):
        st.write("Seuls les fichiers au format `zip` sont pris en charge. Les fichiers doivent respecter la syntaxe suivante : `BrtPdm_CHIMIE_xxxxxxxx.zip` où `xxxxxxx` est une date au format `DDMMYYYY`. Les fichiers doivent contenir les fichiers suivants :")
        st.write('BrtPdm_CHIMIE_xxxxxxxx.zip  \n ├── Pdm_TEI48_Data_xxxxxxxx.txt  \n ├── Pdm_TEI48_Fonct_xxxxxxxx.txt  \n ├── Pdm_TEI48_Zero_xxxxxxxx.txt  \n ├── Pdm_TEI49_Data_xxxxxxxx.txt  \n └── Pdm_TEI49_Fonct_xxxxxxxx.txt')

    with st.expander('Suppression des données'):
        st.write("Si vous importez un nouveau fichier, les données précédemment enregistrées seront automatiquement supprimées.")
        st.write("Les données sont automatiquement supprimées lorsque vous fermez la page ou lorsque vous fermez le navigateur.")
        st.error("Attention, cette action est irréversible !")