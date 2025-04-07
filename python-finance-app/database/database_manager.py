# database/database_manager.py

import mysql.connector
from mysql.connector import Error
from config.db_config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect_to_server(self):
        """Connect to MySQL server (no specific database)"""
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD
            )
            if self.connection.is_connected():
                print("✅ Connected to MySQL server")
        except Error as e:
            print(f"❌ Error connecting to server: {e}")

    def create_database_if_not_exists(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"✅ Database '{DB_NAME}' ensured")
        except Error as e:
            print(f"❌ Failed to create database: {e}")

    def connect_to_database(self):
        """Connect to the actual app database"""
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.connection.is_connected():
                print(f"✅ Connected to database '{DB_NAME}'")
        except Error as e:
            print(f"❌ Error connecting to database: {e}")

    def initialize_tables(self):
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
        """

        transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            category VARCHAR(50),
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """

        self.execute_query(users_table)
        self.execute_query(transactions_table)
        print("✅ Tables initialized")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"❌ Query failed: {e}")
            return None

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Fetch failed: {e}")
            return []

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Connection closed")