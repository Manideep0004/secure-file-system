import sqlite3

def list_users():
    """Display all users in the database"""
    conn = sqlite3.connect('secure_files.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, role FROM users')
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        print("\n❌ No users found in database!")
        return []
    
    print("\n" + "="*60)
    print("📋 CURRENT USERS")
    print("="*60)
    for user in users:
        user_id, username, email, role = user
        print(f"ID: {user_id} | Username: {username} | Email: {email} | Role: {role}")
    print("="*60)
    return users

def promote_to_admin(username):
    """Promote a user to admin role"""
    conn = sqlite3.connect('secure_files.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id, username, role FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"\n❌ User '{username}' not found!")
        conn.close()
        return False
    
    user_id, db_username, current_role = user
    
    if current_role == 'admin':
        print(f"\n✅ User '{username}' is already an admin!")
        conn.close()
        return True
    
    # Update to admin
    cursor.execute('UPDATE users SET role = ? WHERE username = ?', ('admin', username))
    conn.commit()
    conn.close()
    
    print(f"\n✅ SUCCESS! User '{username}' has been promoted to ADMIN!")
    return True

def demote_to_user(username):
    """Demote an admin to regular user"""
    conn = sqlite3.connect('secure_files.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id, username, role FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"\n❌ User '{username}' not found!")
        conn.close()
        return False
    
    user_id, db_username, current_role = user
    
    if current_role == 'user':
        print(f"\n✅ User '{username}' is already a regular user!")
        conn.close()
        return True
    
    # Update to user
    cursor.execute('UPDATE users SET role = ? WHERE username = ?', ('user', username))
    conn.commit()
    conn.close()
    
    print(f"\n✅ SUCCESS! User '{username}' has been demoted to USER!")
    return True

def main():
    print("\n" + "="*60)
    print("🔐 SECURE FILE SYSTEM - USER ROLE MANAGER")
    print("="*60)
    
    while True:
        # List all users
        users = list_users()
        
        if not users:
            print("\n⚠️  Please register a user first through the web interface!")
            break
        
        print("\n📋 OPTIONS:")
        print("1. Promote user to ADMIN")
        print("2. Demote user to USER")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            username = input("\nEnter username to promote to ADMIN: ").strip()
            if username:
                promote_to_admin(username)
            else:
                print("\n❌ Username cannot be empty!")
        
        elif choice == '2':
            username = input("\nEnter username to demote to USER: ").strip()
            if username:
                demote_to_user(username)
            else:
                print("\n❌ Username cannot be empty!")
        
        elif choice == '3':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, or 3.")
        
        continue_choice = input("\nWould you like to make another change? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")