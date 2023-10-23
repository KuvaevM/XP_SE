import unittest
import sqlite3
import os
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

if __name__ == "__main__":
    unittest.main()