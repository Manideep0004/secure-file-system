import streamlit as st
from ui.login_ui import show_login_page
from ui.dashboard_ui import show_dashboard
from ui.file_ui import show_file_manager
from ui.admin_ui import show_admin_panel

st.set_page_config(
    page_title="Secure File Management System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user' not in st.session_state:
    st.session_state.user = None

def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

def main():
    if not st.session_state.authenticated:
        show_login_page()
    else:
        user = st.session_state.user
        
        with st.sidebar:
            st.title("🔐 Secure Files")
            st.write(f"**User:** {user['username']}")
            st.write(f"**Role:** {user['role'].capitalize()}")
            st.divider()
            
            page = st.radio(
                "Navigation",
                ["Dashboard", "File Manager", "Admin Panel"] if user['role'] == 'admin' 
                else ["Dashboard", "File Manager"]
            )
            
            st.divider()
            if st.button("🚪 Logout", use_container_width=True):
                logout()
        
        if page == "Dashboard":
            show_dashboard()
        elif page == "File Manager":
            show_file_manager()
        elif page == "Admin Panel":
            show_admin_panel()

if __name__ == "__main__":
    main()