import streamlit as st

def signup_page():
    st.title("Signup Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Signup"):
        if email and password:
            st.session_state['email'] = email
            st.session_state['password'] = password
            st.session_state['logged_in'] = True
            st.success("Signed up successfully")
            st.rerun()  # Refresh the page to reflect changes
        else:
            st.error("Please enter your email and password")

    st.write("Already have an account?")
    st.markdown("[Go to Login](?page=login)", unsafe_allow_html=True)
