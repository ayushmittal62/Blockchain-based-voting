import sqlite3
import threading
from contextlib import contextmanager
from hashlib import sha256
import datetime
import random
from sys import exit

class BlockChain():
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.connection = None  # Initialize connection as None
                cls._instance.candidates = []  # Initialize candidates list
        return cls._instance

    @contextmanager
    def get_connection(self):
        # Set the encryption key (same key used in app.py)
        key = '12345'  # Replace 'your_key' with your actual encryption key
        
        # Create a new connection if it doesn't exist
        if self.connection is None:
            self.connection = sqlite3.connect('blockchain_database.db')
            self.connection.execute(f'PRAGMA key="{key}"')
            self.connection.execute('PRAGMA cipher_compatibility = 3')  # Use cipher_compatibility mode 3 for SQLCipher 4.x
        
        try:
            yield self.connection
        finally:
            # Close the connection after use
            self.connection.close()
            self.connection = None

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS votes (
                                id INTEGER PRIMARY KEY,
                                voter_name TEXT NOT NULL,
                                voter_id INTEGER NOT NULL,
                                vote_choice TEXT NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )''')

    def insert_vote(self, voter_name, voter_id, vote_choice):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO votes (voter_name, voter_id, vote_choice) VALUES (?, ?, ?)', (voter_name, voter_id, vote_choice))

# Instantiate the blockchain using the Singleton pattern
chain = BlockChain()
