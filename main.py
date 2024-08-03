import streamlit as st
from Auth_login import login_page
from Auth_signup import signup_page
from app import app_page

st.set_page_config(page_title="Multi-Page Streamlit App")

if 'email' not in st.session_state:
    st.session_state['email'] = None

if 'password' not in st.session_state:
    st.session_state['password'] = None

PAGES = {
    "Login": login_page,
    "Signup": signup_page,
    "App": app_page
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page()
