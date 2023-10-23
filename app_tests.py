import unittest
import pytest
import sqlite3
from kivy.tests.common import GraphicUnitTest
from kivy.uix.textinput import TextInput

from app import Database, SignupPage, MyApp

# Поменяйте на имя вашего файла приложения
APP_FILENAME = "your_app.py"


class TestRegistrationProcess(GraphicUnitTest):
    def setUp(self):
        self.app = self.create_app()
        self.db = Database(':memory:')
        self.signup_page = SignupPage(self.db)

    def tearDown(self):
        self.db.close()

    def create_app(self):
        return MyApp.get_running_app()

    def test_successful_registration(self):
        # Ожидается успешная регистрация
        self.signup_page.login.text = "testuser"
        self.signup_page.password.text = "password"
        self.signup_page.repeat_password.text = "password"

        self.signup_page.add_user(None)
        self.assertEqual(self.signup_page.result.text, 'User registered')

        # Проверяем, что пользователь добавлен в базу данных
        self.assertTrue(self.db.user_exists("testuser"))

    def test_password_mismatch(self):
        # Пароли не совпадают
        self.signup_page.login.text = "testuser"
        self.signup_page.password.text = "password"
        self.signup_page.repeat_password.text = "different_password"

        self.signup_page.add_user(None)
        self.assertEqual(self.signup_page.result.text, 'Passwords do not match')

        # Пользователь не должен быть добавлен в базу данных
        self.assertFalse(self.db.user_exists("testuser"))

if __name__ == '__main__':
    unittest.main()
