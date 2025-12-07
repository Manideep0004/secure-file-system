from datetime import datetime

class User:
    def __init__(self, id, username, email, password_hash, role='user'):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

class File:
    def __init__(self, id, owner_id, original_name, encrypted_name, upload_time):
        self.id = id
        self.owner_id = owner_id
        self.original_name = original_name
        self.encrypted_name = encrypted_name
        self.upload_time = upload_time

class Permission:
    def __init__(self, file_id, user_id, can_download=True):
        self.file_id = file_id
        self.user_id = user_id
        self.can_download = can_download

class Log:
    def __init__(self, user_id, action, file_id, timestamp):
        self.user_id = user_id
        self.action = action
        self.file_id = file_id
        self.timestamp = timestamp