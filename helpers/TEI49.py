import streamlit as st


def data_TEI49():
    if 'Pdm_TEI49_Data' in st.session_state:
        TEI49_Data = st.session_state.Pdm_TEI49_Data

        y_data = st.selectbox( 
            'Veuillez choisir les données pour l\'axe x.',
            (col for col in TEI49_Data.columns if col != "valid" and col !='20t_Date'))
        st.line_chart(TEI49_Data, x='20t_Date', y=y_data)
        st.write('Statistiques sur les données brutes')
        st.write(TEI49_Data.describe().loc[['min', 'max', 'mean', 'count']])

        with open('output.txt', 'w') as f:
            f.write(TEI49_Data.describe().loc[['mean']].to_csv(sep='\n'))
    else:
        st.error('Pdm_TEI49_Data n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')
        

def fonct_TEI49():
    if 'Pdm_TEI49_Fonct' in st.session_state:
        TEI49_Fonct = st.session_state.Pdm_TEI49_Fonct
        y_data = st.selectbox( 
            'Veuillez choisir les données pour l\'axe x.',
            (col for col in TEI49_Fonct.columns if col != "valid" and col !='20t_Date'))
        st.line_chart(TEI49_Fonct, x='20t_Date', y=y_data)
        st.write('Statistiques sur les données brutes')
        st.write(TEI49_Fonct.describe().loc[['min', 'max', 'mean', 'count']])

        with open('output.txt', 'w') as f:
            f.write(TEI49_Fonct.describe().loc[['mean']].to_csv(sep='\n'))
    else:
        st.error('Pdm_TEI49_Data n\'est pas dans la session. Merci de charger une archive contenant les données nécessaires.')


def zero_TEI49():
    st.title('TEI 49 Zero')
    st.info('Cet instrument ne fournit pas de données de zéro.')