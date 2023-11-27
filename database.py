import sqlite3
import bcrypt


class Database:

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS users (login TEXT, password TEXT)')
        self.c.execute('CREATE TABLE IF NOT EXISTS messages (title TEXT, message TEXT)')
        self.conn.commit()

    def validate_user(self, user, password):
        self.c.execute("SELECT * FROM users WHERE login=?", (user,))
        user_data = self.c.fetchone()

        if user_data:
            stored_hashed_password = user_data[1]
            return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password)
        else:
            return False

    def user_exists(self, user):
        self.c.execute("SELECT * FROM users WHERE login=?", (user,))
        return bool(self.c.fetchone())

    def add_user(self, user, password):
        hashed_password = self.hash_password(password)

        self.c.execute("INSERT INTO users VALUES (?, ?)", (user, hashed_password))
        self.conn.commit()

    def get_users(self):
        self.c.execute("SELECT * FROM users")
        users_data = self.c.fetchall()

        users = []
        for user_data in users_data:
            user = (user_data[0], user_data[1])
            users.append(user)

        return users

    def add_message(self, title, message):
        self.c.execute("INSERT INTO messages VALUES (?, ?)", (title, message))
        self.conn.commit()

    def get_messages(self):
        self.c.execute("SELECT * FROM messages")
        return [(message[0], message[1]) for message in self.c.fetchall()]

    def delete_message(self, title, message):
        self.c.execute("DELETE FROM messages WHERE title=? AND message=?", (title, message))
        self.conn.commit()

    def delete_message_by_title(self, title):
        self.c.execute('DELETE FROM messages WHERE title = ?', (title,))
        self.conn.commit()

    def close(self):
        self.conn.close()
