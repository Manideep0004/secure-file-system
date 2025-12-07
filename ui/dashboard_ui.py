import streamlit as st
from analytics.stats import Analytics
from core.logs import LogManager

def show_dashboard():
    st.title("📊 Dashboard")
    
    analytics = Analytics()
    log_manager = LogManager()
    user = st.session_state.user
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        file_count = analytics.get_user_file_count(user['id'])
        st.metric("My Files", file_count)
    
    with col2:
        total_files = analytics.get_total_files()
        st.metric("Total Files in System", total_files)
    
    with col3:
        if user['role'] == 'admin':
            total_users = analytics.get_total_users()
            st.metric("Total Users", total_users)
        else:
            st.metric("Account Type", user['role'].capitalize())
    
    st.divider()
    
    st.subheader("📋 Recent Activity")
    recent_activity = log_manager.get_recent_activity(user['id'], limit=10)
    
    if recent_activity:
        for action, timestamp in recent_activity:
            st.text(f"• {action} - {timestamp}")
    else:
        st.info("No recent activity")
    
    st.divider()
    
    if user['role'] == 'admin':
        st.subheader("📈 System Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Most Active Users**")
            active_users = analytics.get_most_active_users(limit=5)
            if not active_users.empty:
                st.dataframe(active_users, use_container_width=True, hide_index=True)
            else:
                st.info("No data available")
        
        with col2:
            st.write("**Most Accessed Files**")
            accessed_files = analytics.get_most_accessed_files(limit=5)
            if not accessed_files.empty:
                st.dataframe(accessed_files, use_container_width=True, hide_index=True)
            else:
                st.info("No data available")