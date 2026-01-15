import sqlite3
from templates.configuration.config import Config
from pathlib import Path


class Database:


    def __init__(self):
        self.db_path = Config.DB_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self):
        connection = sqlite3.connect(self.db_path, timeout=30)
        connection.row_factory = sqlite3.Row
        return connection

    def init_db(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS bids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_id TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        connection.commit()
        cursor.close()
        connection.close()
