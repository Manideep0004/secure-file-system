import pandas as pd
from datetime import datetime, timedelta
from database.db import Database

class Analytics:
    def __init__(self):
        self.db = Database()
    
    def get_total_files(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM files')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_total_users(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_files_uploaded_per_day(self, days=7):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DATE(upload_time) as date, COUNT(*) as count
            FROM files
            WHERE upload_time >= date('now', '-' || ? || ' days')
            GROUP BY DATE(upload_time)
            ORDER BY date
        ''', (days,))
        data = cursor.fetchall()
        conn.close()
        
        df = pd.DataFrame(data, columns=['Date', 'Files Uploaded'])
        return df
    
    def get_most_active_users(self, limit=5):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.username, COUNT(l.id) as activity_count
            FROM users u
            JOIN logs l ON u.id = l.user_id
            GROUP BY u.id
            ORDER BY activity_count DESC
            LIMIT ?
        ''', (limit,))
        data = cursor.fetchall()
        conn.close()
        
        df = pd.DataFrame(data, columns=['Username', 'Activity Count'])
        return df
    
    def get_most_accessed_files(self, limit=5):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.original_name, COUNT(l.id) as access_count
            FROM files f
            JOIN logs l ON f.id = l.file_id
            WHERE l.action LIKE '%download%'
            GROUP BY f.id
            ORDER BY access_count DESC
            LIMIT ?
        ''', (limit,))
        data = cursor.fetchall()
        conn.close()
        
        df = pd.DataFrame(data, columns=['File Name', 'Access Count'])
        return df
    
    def get_user_file_count(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM files WHERE owner_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_action_distribution(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT action, COUNT(*) as count
            FROM logs
            GROUP BY action
            ORDER BY count DESC
        ''')
        data = cursor.fetchall()
        conn.close()
        
        df = pd.DataFrame(data, columns=['Action', 'Count'])
        return df