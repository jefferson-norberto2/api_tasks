import sqlite3

class Database:
    def __init__(self, database_path):
        self._connection = sqlite3.connect(database_path)
        self._cursor = self._connection.cursor()

    def execute_query(self, query, values=None):
        if values:
            self._cursor.execute(query, values)
        else:
            self._cursor.execute(query)
        self._connection.commit()

    def fetch_all(self, query, values=None):
        self.execute_query(query, values)
        return self._cursor.fetchall()
    
    def fetch_one(self, query, values):
        self.execute_query(query, values)
        return self._cursor.fetchone()
    
    def close_connection(self):
        self._cursor.close()
        self._connection.close()
