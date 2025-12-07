from database.db import Database

class LogManager:
    def __init__(self):
        self.db = Database()
    
    def log_action(self, user_id, action, file_id=None):
        self.db.create_log(user_id, action, file_id)
    
    def get_user_logs(self, user_id, limit=10):
        return self.db.get_logs_by_user(user_id, limit)
    
    def get_all_logs(self, limit=100):
        return self.db.get_all_logs(limit)
    
    def get_recent_activity(self, user_id, limit=5):
        return self.db.get_recent_activity(user_id, limit)
    