import sqlite3

class Database:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS users (login TEXT, password TEXT)')
        self.conn.commit()

    def validate_user(self, user, password):
        self.c.execute("SELECT * FROM users WHERE login=? AND password=?", (user, password))
        return bool(self.c.fetchone())

    def user_exists(self, user):
        self.c.execute("SELECT * FROM users WHERE login=?", (user,))
        return bool(self.c.fetchone())

    def add_user(self, user, password):
        self.c.execute("INSERT INTO users VALUES (?, ?)", (user, password))
        self.conn.commit()

    def close(self):
        self.conn.close()