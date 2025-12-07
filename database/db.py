import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='secure_files.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')
        
        # Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                original_name TEXT NOT NULL,
                encrypted_name TEXT NOT NULL,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
        ''')
        
        # Permissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                can_download INTEGER DEFAULT 1,
                FOREIGN KEY (file_id) REFERENCES files(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                file_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # User operations
    def create_user(self, username, email, password_hash, role='user'):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                (username, email, password_hash, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None
    
    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def get_user_by_id(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, role FROM users')
        users = cursor.fetchall()
        conn.close()
        return users
    
    def update_user_role(self, user_id, new_role):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
        conn.commit()
        conn.close()
    
    # File operations
    def create_file(self, owner_id, original_name, encrypted_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO files (owner_id, original_name, encrypted_name) VALUES (?, ?, ?)',
            (owner_id, original_name, encrypted_name)
        )
        conn.commit()
        file_id = cursor.lastrowid
        conn.close()
        return file_id
    
    def get_files_by_owner(self, owner_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM files WHERE owner_id = ?', (owner_id,))
        files = cursor.fetchall()
        conn.close()
        return files
    
    def get_file_by_id(self, file_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM files WHERE id = ?', (file_id,))
        file = cursor.fetchone()
        conn.close()
        return file
    
    def get_all_files(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.id, f.original_name, u.username, f.upload_time 
            FROM files f 
            JOIN users u ON f.owner_id = u.id
        ''')
        files = cursor.fetchall()
        conn.close()
        return files
    
    def delete_file(self, file_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files WHERE id = ?', (file_id,))
        cursor.execute('DELETE FROM permissions WHERE file_id = ?', (file_id,))
        conn.commit()
        conn.close()
    
    def get_shared_files(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.* FROM files f
            JOIN permissions p ON f.id = p.file_id
            WHERE p.user_id = ? AND f.owner_id != ?
        ''', (user_id, user_id))
        files = cursor.fetchall()
        conn.close()
        return files
    
    # Permission operations
    def create_permission(self, file_id, user_id, can_download=True):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO permissions (file_id, user_id, can_download) VALUES (?, ?, ?)',
                (file_id, user_id, int(can_download))
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def check_permission(self, file_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT can_download FROM permissions WHERE file_id = ? AND user_id = ?',
            (file_id, user_id)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_file_permissions(self, file_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.username, p.can_download 
            FROM permissions p
            JOIN users u ON p.user_id = u.id
            WHERE p.file_id = ?
        ''', (file_id,))
        permissions = cursor.fetchall()
        conn.close()
        return permissions
    
    # Log operations
    def create_log(self, user_id, action, file_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO logs (user_id, action, file_id) VALUES (?, ?, ?)',
            (user_id, action, file_id)
        )
        conn.commit()
        conn.close()
    
    def get_logs_by_user(self, user_id, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
            (user_id, limit)
        )
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    def get_all_logs(self, limit=100):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT l.id, u.username, l.action, l.file_id, l.timestamp 
            FROM logs l
            JOIN users u ON l.user_id = u.id
            ORDER BY l.timestamp DESC
            LIMIT ?
        ''', (limit,))
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    def get_recent_activity(self, user_id, limit=5):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT action, timestamp FROM logs 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
        activity = cursor.fetchall()
        conn.close()
        return activity