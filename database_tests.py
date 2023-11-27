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

    def test_add_and_get_messages(self):
        messages = ["Hello, World!", "Testing 123", "Another message"]
        for message in messages:
            self.db.add_message(message)

        retrieved_messages = self.db.get_messages()

        self.assertEqual(retrieved_messages, messages)

    def test_add_and_get_users(self):
        users = [("user1", "password1"), ("user2", "password2"), ("user3", "password3")]
        for user, password in users:
            self.db.add_user(user, password)

        retrieved_users = self.db.get_users()

        # Check the equality of logins and verify passwords using bcrypt.checkpw
        for expected_user, retrieved_user in zip(users, retrieved_users):
            expected_login, expected_password = expected_user
            retrieved_login, retrieved_hashed_password = retrieved_user

            # Check login equality
            self.assertEqual(expected_login, retrieved_login)

            # Verify password using bcrypt.checkpw
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


if __name__ == "__main__":
    unittest.main()
