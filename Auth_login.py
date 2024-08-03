import streamlit as st

def login_page():
    st.title("Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if email and password:
            st.session_state['email'] = email
            st.session_state['password'] = password
            return email, password
        else:
            st.error("Please enter your email and password")

    st.write("Don't have an account?")
    st.markdown("[Go to Signup](?page=signup)", unsafe_allow_html=True)
