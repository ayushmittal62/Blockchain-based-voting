import sqlite3
import vote_chain

class BlockChain():
    def __init__(self):
        self.connection = None
        self.israel_election = self  # Make the instance available for other modules

    def connect_database(self):
        # Set the encryption key (same key used in vote_chain.py)
        key = '12345'  # Replace 'your_key' with your actual encryption key
        
        # Connect to the SQLite database with encryption using SQLCipher
        conn = sqlite3.connect('blockchain_database.db')
        conn.execute(f'PRAGMA key="{key}"')
        conn.execute('PRAGMA cipher_compatibility = 3')  # Use cipher_compatibility mode 3 for SQLCipher 4.x
        return conn

    def create_tables(self):
        with self.connect_database() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS votes (
                                id INTEGER PRIMARY KEY,
                                voter_name TEXT NOT NULL,
                                voter_id INTEGER NOT NULL,
                                vote_choice TEXT NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )''')
            conn.commit()
            print("Database and tables created successfully.")  # Add debug statement

    def close_database(self):
        if self.connection:
            self.connection.close()

    def insert_vote(self, voter_name, voter_id, vote_choice):
        with self.connect_database() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO votes (voter_name, voter_id, vote_choice) VALUES (?, ?, ?)', (voter_name, voter_id, vote_choice))
            conn.commit()

# Instantiate the blockchain
chain = BlockChain()
chain.create_tables()  # Call create_tables method to create the database and tables
