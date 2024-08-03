import streamlit as st

def tmp_page():
    st.title("Temp Page")
    st.write("This is a temporary page")

    st.markdown("[Go to Login](?page=login)", unsafe_allow_html=True)
    st.markdown("[Go to Signup](?page=signup)", unsafe_allow_html=True)
