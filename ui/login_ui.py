import streamlit as st
from core.auth import AuthManager

def show_login_page():
    auth = AuthManager()
    
    st.title("🔐 Secure File Management System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if login_username and login_password:
                user, message = auth.login_user(login_username, login_password)
                if user:
                    st.session_state.user = user
                    st.session_state.authenticated = True
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.subheader("Register New Account")
        reg_username = st.text_input("Username", key="reg_username")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", key="register_button"):
            if reg_username and reg_email and reg_password and reg_confirm_password:
                if reg_password != reg_confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = auth.register_user(reg_username, reg_email, reg_password)
                    if success:
                        st.success(message)
                        st.info("Please login with your credentials")
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all fields")