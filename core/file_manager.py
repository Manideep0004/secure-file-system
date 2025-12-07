import os
import uuid
from datetime import datetime
from database.db import Database
from core.encryption import EncryptionManager

class FileManager:
    def __init__(self, storage_path='storage'):
        self.storage_path = storage_path
        self.db = Database()
        self.encryption = EncryptionManager()
        
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
    
    def upload_file(self, file_data, original_name, owner_id):
        try:
            encrypted_data = self.encryption.encrypt_file(file_data)
            encrypted_name = f"{uuid.uuid4().hex}_{original_name}"
            file_path = os.path.join(self.storage_path, encrypted_name)
            
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            file_id = self.db.create_file(owner_id, original_name, encrypted_name)
            self.db.create_log(owner_id, 'File uploaded', file_id)
            
            return True, file_id, "File uploaded successfully"
        except Exception as e:
            return False, None, f"Upload failed: {str(e)}"
    
    def download_file(self, file_id, user_id):
        try:
            file_record = self.db.get_file_by_id(file_id)
            
            if not file_record:
                return None, None, "File not found"
            
            file_db_id, owner_id, original_name, encrypted_name, upload_time = file_record
            
            if owner_id != user_id:
                permission = self.db.check_permission(file_id, user_id)
                if permission is None or permission == 0:
                    return None, None, "Access denied"
            
            file_path = os.path.join(self.storage_path, encrypted_name)
            
            if not os.path.exists(file_path):
                return None, None, "File not found on disk"
            
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.encryption.decrypt_file(encrypted_data)
            self.db.create_log(user_id, 'File downloaded', file_id)
            
            return decrypted_data, original_name, "File downloaded successfully"
        except Exception as e:
            return None, None, f"Download failed: {str(e)}"
    
    def delete_file(self, file_id, user_id):
        try:
            file_record = self.db.get_file_by_id(file_id)
            
            if not file_record:
                return False, "File not found"
            
            file_db_id, owner_id, original_name, encrypted_name, upload_time = file_record
            
            if owner_id != user_id:
                user = self.db.get_user_by_id(user_id)
                if not user or user[4] != 'admin':
                    return False, "Access denied"
            
            file_path = os.path.join(self.storage_path, encrypted_name)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            self.db.delete_file(file_id)
            self.db.create_log(user_id, 'File deleted', file_id)
            
            return True, "File deleted successfully"
        except Exception as e:
            return False, f"Delete failed: {str(e)}"
    
    def get_user_files(self, user_id):
        return self.db.get_files_by_owner(user_id)
    
    def get_shared_files(self, user_id):
        return self.db.get_shared_files(user_id)
    
    def get_all_files(self):
        return self.db.get_all_files()