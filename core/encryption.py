from cryptography.fernet import Fernet
import os

class EncryptionManager:
    def __init__(self, key_file='encryption.key'):
        self.key_file = key_file
        self.key = self.load_or_generate_key()
        self.cipher = Fernet(self.key)
    
    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_file(self, file_data):
        return self.cipher.encrypt(file_data)
    
    def decrypt_file(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data)
    
    def encrypt_text(self, text):
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt_text(self, encrypted_text):
        return self.cipher.decrypt(encrypted_text.encode()).decode()