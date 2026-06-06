import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name='portfolio.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS capital (
                id INTEGER PRIMARY KEY,
                amount REAL NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                stock_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                buy_price REAL NOT NULL,
                sell_price REAL,
                status TEXT DEFAULT 'open',
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_sold TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_capital(self, amount):
        self.cursor.execute('INSERT INTO capital (amount) VALUES (?)', (amount,))
        self.conn.commit()
    
    def set_capital(self, amount):
        self.cursor.execute('DELETE FROM capital')
        self.cursor.execute('INSERT INTO capital (amount) VALUES (?)', (amount,))
        self.conn.commit()

    def get_capital(self):
        self.cursor.execute('SELECT SUM(amount) FROM capital')
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0
    
    def add_transaction(self, stock_name, quantity, buy_price):
        self.cursor.execute('''
            INSERT INTO transactions (stock_name, quantity, buy_price, status)
            VALUES (?, ?, ?, 'open')
        ''', (stock_name, quantity, buy_price))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def close_transaction(self, transaction_id, sell_price):
        self.cursor.execute('''
            UPDATE transactions 
            SET sell_price = ?, status = 'closed', date_sold = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (sell_price, transaction_id))
        self.conn.commit()
    
    def get_all_transactions(self):
        self.cursor.execute('SELECT * FROM transactions')
        return self.cursor.fetchall()
    
    def get_transaction(self, transaction_id):
        self.cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        return self.cursor.fetchone()
    
    def delete_transaction(self, transaction_id):
        self.cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        self.conn.commit()
    
    def close_database(self):
        if self.conn:
            self.conn.close()
