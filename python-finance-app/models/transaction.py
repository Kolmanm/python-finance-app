# models/transaction.py

from database.database_manager import DatabaseManager
from datetime import datetime

class Transaction:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add(self, user_id, amount, category=None, description=None):
        query = """
        INSERT INTO transactions (user_id, amount, category, description)
        VALUES (%s, %s, %s, %s)
        """
        tx_id = self.db.execute_query(query, (user_id, amount, category, description))
        if tx_id:
            print(f"✅ Transaction added (ID: {tx_id})")
            return tx_id
        print("❌ Failed to add transaction")
        return None

    def delete(self, transaction_id, user_id):
        query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
        rows = self.db.execute_query(query, (transaction_id, user_id))
        if rows is not None:
            print(f"🗑️ Transaction {transaction_id} deleted")
            return True
        print("❌ Failed to delete transaction")
        return False

    def get_all_for_user(self, user_id):
        query = """
        SELECT * FROM transactions
        WHERE user_id = %s
        ORDER BY date DESC
        """
        return self.db.fetch_all(query, (user_id,))