import streamlit as st

from helpers import home_page, data_page, instruments_page
from helpers.utils import show_Laero_logo

def main():
    st.set_page_config(
        page_title="BE",
        # page_icon="https://sersitive.eu/wp-content/uploads/cropped-icon.png",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    html_code = show_Laero_logo(100, [1, 1, 1, 1], margin=[0, 0, 0, 0])
    st.sidebar.markdown(html_code, unsafe_allow_html=True)

    page = st.sidebar.selectbox("Pages", ['Accueil', 'Données', 'Instruments'])

    if page == 'Accueil':
        home_page.main()
    if page == 'Données':
        data_page.main()
    if page == 'Instruments':
        instruments_page.main()


if __name__ == '__main__':
    main()