import unittest
import sqlite3
import os
import bcrypt
import unittest
from database import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get_users(self):
        users = [("user1", "password1"), ("user2", "password2"), ("user3", "password3")]
        for user, password in users:
            self.db.add_user(user, password)

        retrieved_users = self.db.get_users()

        for expected_user, retrieved_user in zip(users, retrieved_users):
            expected_login, expected_password = expected_user
            retrieved_login, retrieved_hashed_password = retrieved_user

            self.assertEqual(expected_login, retrieved_login)

            self.assertTrue(bcrypt.checkpw(expected_password.encode('utf-8'), retrieved_hashed_password))

    def test_validate_user(self):
        user = "test_user"
        password = "test_password"
        self.db.add_user(user, password)

        self.assertTrue(self.db.validate_user(user, password))

        self.assertFalse(self.db.validate_user(user, "wrong_password"))

    def test_user_exists(self):
        user = "existing_user"
        self.db.add_user(user, "password")

        self.assertTrue(self.db.user_exists(user))

        self.assertFalse(self.db.user_exists("non_existing_user"))

    def test_add_message(self):
        title = "Test Title"
        message = "Test Message"
        self.db.add_message(title, message)

        messages = self.db.get_messages()
        self.assertIn(f"{title}: {message}", messages)

    def test_get_messages(self):
        messages = self.db.get_messages()
        self.assertEqual(messages, [])

        self.db.add_message("Title 1", "Message 1")
        self.db.add_message("Title 2", "Message 2")

        messages = self.db.get_messages()
        self.assertEqual(messages, ["Title 1: Message 1", "Title 2: Message 2"])

    def test_delete_message(self):
        title = "Test Title"
        message = "Test Message"
        self.db.add_message(title, message)

        messages_before_deletion = self.db.get_messages()
        self.assertIn(f"{title}: {message}", messages_before_deletion)

        self.db.delete_message(title, message)

        messages_after_deletion = self.db.get_messages()
        self.assertNotIn(f"{title}: {message}", messages_after_deletion)

    def test_delete_nonexistent_message(self):
        title = "Nonexistent Title"
        message = "Nonexistent Message"

        self.db.delete_message(title, message)


if __name__ == "__main__":
    unittest.main()
