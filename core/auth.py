import bcrypt
from database.db import Database

class AuthManager:
    def __init__(self):
        self.db = Database()
    
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, password_hash):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def register_user(self, username, email, password, role='user'):
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if not username or not email:
            return False, "Username and email are required"
        
        password_hash = self.hash_password(password)
        user_id = self.db.create_user(username, email, password_hash, role)
        
        if user_id:
            self.db.create_log(user_id, 'User registered')
            return True, "Registration successful"
        else:
            return False, "Username or email already exists"
    
    def login_user(self, username, password):
        user = self.db.get_user_by_username(username)
        
        if not user:
            return None, "Invalid username or password"
        
        user_id, db_username, email, password_hash, role = user
        
        if self.verify_password(password, password_hash):
            self.db.create_log(user_id, 'User logged in')
            return {
                'id': user_id,
                'username': db_username,
                'email': email,
                'role': role
            }, "Login successful"
        else:
            return None, "Invalid username or password"
    
    def is_admin(self, user_id):
        user = self.db.get_user_by_id(user_id)
        if user:
            return user[4] == 'admin'
        return False