import unittest
from unittest.mock import Mock
from app import MyApp


class TestMyApp(unittest.TestCase):

    def setUp(self):
        self.app = MyApp()

    def test_login_failure(self):
        self.app.db = Mock()
        self.app.db.validate_user.return_value = False

        self.app.build()
        self.app.show_login(None)

        self.app.login_page.login.text = 'testuser'
        self.app.login_page.password.text = 'wrongpassword'
        self.app.login_page.validate_user(None)

        self.assertEqual(self.app.login_page.result.text, 'Not OK')

    def test_signup_failure_user_exists(self):
        self.app.db = Mock()
        self.app.db.user_exists.return_value = True

        self.app.build()
        self.app.show_signup(None)

        self.app.signup_page.login.text = 'existinguser'
        self.app.signup_page.password.text = 'newpassword'
        self.app.signup_page.repeat_password.text = 'newpassword'
        self.app.signup_page.add_user(None)

        self.assertEqual(self.app.signup_page.result.text, 'User already exists')

    def test_signup_failure_password_mismatch(self):
        self.app.db = Mock()
        self.app.db.user_exists.return_value = False

        self.app.build()
        self.app.show_signup(None)

        self.app.signup_page.login.text = 'newuser'
        self.app.signup_page.password.text = 'newpassword'
        self.app.signup_page.repeat_password.text = 'differentpassword'
        self.app.signup_page.add_user(None)

        self.assertEqual(self.app.signup_page.result.text, 'Passwords do not match')

    def test_back_to_main_menu_from_login(self):
        self.app.db = Mock()

        self.app.build()
        self.app.show_login(None)

        self.assertIs(self.app.root.children[0], self.app.login_page)

        back_btn = self.app.login_page.children[0]
        back_btn.dispatch('on_press')

        self.assertIs(self.app.root.children[0], self.app.start_page)

    def test_back_to_main_menu_from_signup(self):
        self.app.db = Mock()

        self.app.build()
        self.app.show_signup(None)

        self.assertIs(self.app.root.children[0], self.app.signup_page)

        back_btn = self.app.signup_page.children[0]
        back_btn.dispatch('on_press')

        self.assertIs(self.app.root.children[0], self.app.start_page)

if __name__ == '__main__':
    unittest.main()