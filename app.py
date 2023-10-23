import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from database import Database

kivy.require('1.11.1')


class LoginPage(BoxLayout):
    def __init__(self, db, app, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.db = db
        self.app = app

        self.add_widget(Label(text='Login'))
        self.login = TextInput(multiline=False)
        self.add_widget(self.login)

        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.login_btn = Button(text='Sign In')
        self.login_btn.bind(on_press=self.validate_user)
        self.add_widget(self.login_btn)

        self.result = Label(text='')
        self.add_widget(self.result)

        self.add_back_button()

    def validate_user(self, instance):
        user = self.login.text
        password = self.password.text

        if self.db.validate_user(user, password):
            self.result.text = 'OK'
        else:
            self.result.text = 'Not OK'

    def add_back_button(self):
        back_btn = Button(text='Back to Main Menu')
        back_btn.bind(on_press=self.app.show_start_page)
        self.add_widget(back_btn)

class SignupPage(BoxLayout):
    def __init__(self, db, app, **kwargs):
        super(SignupPage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.db = db
        self.app = app

        self.add_widget(Label(text='Login'))
        self.login = TextInput(multiline=False)
        self.add_widget(self.login)

        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.add_widget(Label(text='Repeat Password'))
        self.repeat_password = TextInput(password=True, multiline=False)
        self.add_widget(self.repeat_password)

        self.signup_btn = Button(text='Sign Up')
        self.signup_btn.bind(on_press=self.add_user)
        self.add_widget(self.signup_btn)

        self.result = Label(text='')
        self.add_widget(self.result)

        self.add_back_button()

    def add_user(self, instance):
        user = self.login.text
        password = self.password.text
        repeat_password = self.repeat_password.text

        if password != repeat_password:
            self.result.text = 'Passwords do not match'
            return

        if self.db.user_exists(user):
            self.result.text = 'User already exists'
        else:
            self.db.add_user(user, password)
            self.result.text = 'User registered'

    def add_back_button(self):
        back_btn = Button(text='Back to Main Menu')
        back_btn.bind(on_press=self.app.show_start_page)
        self.add_widget(back_btn)

class MyApp(App):
    def build(self):
        self.db = Database()

        self.root = BoxLayout(orientation='vertical')
        self.login_page = LoginPage(self.db, app=self)
        self.signup_page = SignupPage(self.db, app=self)
        self.start_page = BoxLayout(orientation='vertical')

        self.signin_btn = Button(text='Sign In')
        self.signin_btn.bind(on_press=self.show_login)
        self.start_page.add_widget(self.signin_btn)

        self.signup_btn = Button(text='Sign Up')
        self.signup_btn.bind(on_press=self.show_signup)
        self.start_page.add_widget(self.signup_btn)

        self.root.add_widget(self.start_page)
        return self.root

    def show_login(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.login_page)

    def show_signup(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.signup_page)

    def show_start_page(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.start_page)

    def on_stop(self):
        self.db.close()

if __name__ == '__main__':
    MyApp().run()