import streamlit as st
from core.file_manager import FileManager
from core.permissions import PermissionManager
from database.db import Database

def show_file_manager():
    st.title("📁 File Manager")
    
    file_manager = FileManager()
    permission_manager = PermissionManager()
    db = Database()
    user = st.session_state.user
    
    tab1, tab2, tab3 = st.tabs(["My Files", "Shared With Me", "Upload New File"])
    
    with tab1:
        st.subheader("My Files")
        my_files = file_manager.get_user_files(user['id'])
        
        if my_files:
            for file_record in my_files:
                file_id, owner_id, original_name, encrypted_name, upload_time = file_record
                
                with st.expander(f"📄 {original_name}"):
                    st.text(f"Uploaded: {upload_time}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("Download", key=f"download_{file_id}"):
                            data, filename, message = file_manager.download_file(file_id, user['id'])
                            if data:
                                st.download_button(
                                    label="💾 Save File",
                                    data=data,
                                    file_name=filename,
                                    key=f"save_{file_id}"
                                )
                                st.success(message)
                            else:
                                st.error(message)
                    
                    with col2:
                        if st.button("Delete", key=f"delete_{file_id}"):
                            success, message = file_manager.delete_file(file_id, user['id'])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    
                    with col3:
                        with st.popover("Share"):
                            all_users = db.get_all_users()
                            user_options = [u[1] for u in all_users if u[0] != user['id']]
                            
                            selected_user = st.selectbox(
                                "Select User",
                                user_options,
                                key=f"share_user_{file_id}"
                            )
                            
                            if st.button("Grant Access", key=f"grant_{file_id}"):
                                target_user = [u for u in all_users if u[1] == selected_user]
                                if target_user:
                                    success, msg = permission_manager.grant_permission(
                                        file_id, target_user[0][0], user['id']
                                    )
                                    if success:
                                        st.success(msg)
                                    else:
                                        st.error(msg)
        else:
            st.info("No files uploaded yet")
    
    with tab2:
        st.subheader("Shared With Me")
        shared_files = file_manager.get_shared_files(user['id'])
        
        if shared_files:
            for file_record in shared_files:
                file_id, owner_id, original_name, encrypted_name, upload_time = file_record
                
                with st.expander(f"📄 {original_name} (shared)"):
                    st.text(f"Uploaded: {upload_time}")
                    
                    if st.button("Download", key=f"download_shared_{file_id}"):
                        data, filename, message = file_manager.download_file(file_id, user['id'])
                        if data:
                            st.download_button(
                                label="💾 Save File",
                                data=data,
                                file_name=filename,
                                key=f"save_shared_{file_id}"
                            )
                            st.success(message)
                        else:
                            st.error(message)
        else:
            st.info("No files shared with you")
    
    with tab3:
        st.subheader("Upload New File")
        uploaded_file = st.file_uploader("Choose a file", type=None)
        
        if uploaded_file is not None:
            st.info(f"File: {uploaded_file.name} ({uploaded_file.size} bytes)")
            
            if st.button("Upload File"):
                file_data = uploaded_file.read()
                success, file_id, message = file_manager.upload_file(
                    file_data, uploaded_file.name, user['id']
                )
                
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)