import streamlit as st
from database.db import Database
from analytics.stats import Analytics
from core.file_manager import FileManager
import plotly.express as px

def show_admin_panel():
    st.title("⚙️ Admin Panel")
    
    user = st.session_state.user
    
    if user['role'] != 'admin':
        st.error("Access Denied: Admin privileges required")
        return
    
    db = Database()
    analytics = Analytics()
    file_manager = FileManager()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Users", "All Files", "Logs", "Analytics"])
    
    with tab1:
        st.subheader("👥 User Management")
        all_users = db.get_all_users()
        
        if all_users:
            for user_record in all_users:
                user_id, username, email, role = user_record
                
                with st.expander(f"👤 {username} ({role})"):
                    st.text(f"Email: {email}")
                    st.text(f"Role: {role}")
                    
                    new_role = st.selectbox(
                        "Change Role",
                        ["user", "admin"],
                        index=0 if role == "user" else 1,
                        key=f"role_{user_id}"
                    )
                    
                    if st.button("Update Role", key=f"update_{user_id}"):
                        if new_role != role:
                            db.update_user_role(user_id, new_role)
                            st.success(f"Role updated to {new_role}")
                            st.rerun()
                        else:
                            st.info("No change in role")
        else:
            st.info("No users found")
    
    with tab2:
        st.subheader("📂 All Files in System")
        all_files = file_manager.get_all_files()
        
        if all_files:
            for file_record in all_files:
                file_id, original_name, owner_username, upload_time = file_record
                
                with st.expander(f"📄 {original_name}"):
                    st.text(f"Owner: {owner_username}")
                    st.text(f"Uploaded: {upload_time}")
                    st.text(f"File ID: {file_id}")
                    
                    if st.button("Delete File", key=f"admin_delete_{file_id}"):
                        success, message = file_manager.delete_file(file_id, st.session_state.user['id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("No files in system")
    
    with tab3:
        st.subheader("📋 System Logs")
        log_limit = st.slider("Number of logs to display", 10, 200, 50)
        all_logs = db.get_all_logs(limit=log_limit)
        
        if all_logs:
            st.dataframe(
                [{
                    "ID": log[0],
                    "User": log[1],
                    "Action": log[2],
                    "File ID": log[3] if log[3] else "N/A",
                    "Timestamp": log[4]
                } for log in all_logs],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No logs available")
    
    with tab4:
        st.subheader("📊 System Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_files = analytics.get_total_files()
            st.metric("Total Files", total_files)
        
        with col2:
            total_users = analytics.get_total_users()
            st.metric("Total Users", total_users)
        
        st.divider()
        
        st.subheader("📈 Files Uploaded Per Day")
        days = st.slider("Days to show", 3, 30, 7)
        files_per_day = analytics.get_files_uploaded_per_day(days=days)
        
        if not files_per_day.empty:
            fig = px.line(
                files_per_day,
                x='Date',
                y='Files Uploaded',
                title='Files Uploaded Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected period")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Most Active Users")
            active_users = analytics.get_most_active_users(limit=10)
            if not active_users.empty:
                fig = px.bar(
                    active_users,
                    x='Username',
                    y='Activity Count',
                    title='User Activity'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col2:
            st.subheader("📁 Most Accessed Files")
            accessed_files = analytics.get_most_accessed_files(limit=10)
            if not accessed_files.empty:
                fig = px.bar(
                    accessed_files,
                    x='File Name',
                    y='Access Count',
                    title='File Access Count'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        st.divider()
        
        st.subheader("🔄 Action Distribution")
        action_dist = analytics.get_action_distribution()
        if not action_dist.empty:
            fig = px.pie(
                action_dist,
                values='Count',
                names='Action',
                title='Distribution of Actions'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")