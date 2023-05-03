import streamlit as st

def main():
    st.header('Outils de visualisation des données météorologiques et chimiques')

    st.write("Cet outil permet de visualiser les données provenant d'un analyseur d'ozone et d'un analyseur de monoxyde de carbone (sous forme graphique).")
    st.write("👈 Commencez par choisir l'origine de données, et puis soit mettez en ligne un fichier local, soit saisissez l'adresse du serveur distant !")