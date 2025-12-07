from database.db import Database

class PermissionManager:
    def __init__(self):
        self.db = Database()
    
    def grant_permission(self, file_id, user_id, owner_id):
        file_record = self.db.get_file_by_id(file_id)
        
        if not file_record:
            return False, "File not found"
        
        if file_record[1] != owner_id:
            return False, "Only the file owner can grant permissions"
        
        if file_record[1] == user_id:
            return False, "Cannot grant permission to yourself"
        
        success = self.db.create_permission(file_id, user_id, can_download=True)
        
        if success:
            self.db.create_log(owner_id, f'Granted permission for file', file_id)
            return True, "Permission granted successfully"
        else:
            return False, "Permission already exists or failed to grant"
    
    def check_access(self, file_id, user_id):
        file_record = self.db.get_file_by_id(file_id)
        
        if not file_record:
            return False
        
        if file_record[1] == user_id:
            return True
        
        permission = self.db.check_permission(file_id, user_id)
        return permission == 1 if permission is not None else False
    
    def get_file_permissions(self, file_id):
        return self.db.get_file_permissions(file_id)
    