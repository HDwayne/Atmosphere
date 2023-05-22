# Project description

Développer un outil permettant de visualiser les données sous forme graphique. Ces données proviennent d'un analyseur d'ozone et d'un analyseur de monoxyde de carbone. S'il reste du temps en fin de stage, la gestion d'un instrument de mesure des oxydes d'azote est souhaitable.
Plusieurs fichiers sont rattachés à un instrument : Les données proprement dites et les paramètres de fonctionnement de l'instrument : température de fonctionnement, débit des pompes ...
Différentes interactions avec l'interface devront permettre d'invalider les données ou de faire des corrections simples, puis de sauvegarder les données validées et moyennées dans un nouveau fichier contenant dans ces métadonnées les informations de corrections.
Actuellement les fichiers de données sont au format csv mais une gestion du format NetCdf des donnés finales est à prévoir pour une évolution ultérieure.

# Requirements

- Les données à analyser sont regroupées dans des **archives compressées journalières**. Celles-ci sont disponibles, soit dans un répertoire local, soit sur un serveur distant. **Celles-ci ne seront pas modifiées**.
- A l'issue de l'**analyse des données**, les teneurs en gaz devront être moyennées puis sauvegardées dans un fichier au format texte selon un format qui sera fourni en exemple. Le fichier devra être déposé soit dans un répertoire local, soit envoyé sur un serveur distant.
- Les données des instruments devront être **regroupées par onglet**. Chaque onglet devra contenir un graphe représentant la concentration du gaz ainsi que les valeurs **min**, **max** et **moyennes**. Les données des paramètres de fonctionnement seront également représentées sous forme graphique.
- Les **données liées à des paramètres de fonctionnement incorrects** devront être affichée dans une **couleur visible**.
- Il devra être possible d'**invalider les données** liées aux paramètres de fonctionnement incorrect ou à un intervalle de temps choisi par l'utilisateur.
- Il devra être possible de lisser une partie ou toutes les données par un filtre **ébarbeur**.
- Les **paramètres de configuration de l'outil** seront rassemblés dans un fichier de configuration au format **yaml** contenant par exemple le nom des répertoires des fichiers de données, des données corrigées, des images, le nom et l'arborescence des paramètres du réseau.
- Actuellement les fichiers de données sont au **format csv** mais une gestion du **format NetCdf** des donnés finales est à prévoir pour une évolution ultérieure.
- L'outil sera développé en langage **Python**.

# Installation

create a virtual environment and install the requirements

```	
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

deactivate
```

**nb**: if you are using windows, use the following command to activate the virtual environment
```
venv\Scripts\activate.bat
```
and in powershell
```
venv\Scripts\Activate.ps1
```

# Run the app

```
streamlit run app.py
```

# jupyter notebook installation

install directly in the virtual environment

```
pip install ipykernel

python -m ipykernel install --user --name=venv
```

# homepage choice

```
# choice = st.radio(
#     "📊 Sélectionnez la source de données",
#     ("📁 Fichier local", "📥 Serveur distant")
# )
# if choice == "📁 Fichier local":
#     file = st.file_uploader("Veuillez choisir un fichier",
#                             accept_multiple_files=False,
#                             type=['zip'])
# elif choice == "📥 Serveur distant":
#     site = st.text_input("Saisissez l'adresse du serveur 👇")
```
  
```
# if choice == "📁 Fichier local" and file is not None:
```
