# models/user.py

from database.database_manager import DatabaseManager
import bcrypt

class User:
    def __init__(self, db: DatabaseManager, user_id=None, username=None, email=None):
        self.db = db
        self.id = user_id
        self.username = username
        self.email = email
      

    def register(self, username, email, password):
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        query = """
        INSERT INTO users (username, email, password) 
        VALUES (%s, %s, %s)
        """
        user_id = self.db.execute_query(query, (username, email, hashed_pw))
        if user_id:
            print("✅ User registered")
            self.id = user_id
            self.username = username
            self.email = email
            return True
        else:
            print("❌ Registration failed")
            return False

    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s"
        user = self.db.fetch_all(query, (username,))
        if user:
            user = user[0]
            if bcrypt.checkpw(password.encode(), user['password'].encode()):
                print("✅ Login successful")
                self.id = user['id']
                self.username = user['username']
                self.email = user['email']
                return True
        print("❌ Login failed")
        return False

    def delete(self):
        if self.id:
            query = "DELETE FROM users WHERE id = %s"
            self.db.execute_query(query, (self.id,))
            print(f"🗑️ User {self.username} deleted")
            self.id = None
            return True
        return False

    def get_transactions(self):
        if not self.id:
            print("⚠️ No user loaded")
            return []
        query = "SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC"
        return self.db.fetch_all(query, (self.id,))