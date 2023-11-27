import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
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
            self.app.show_message_page()
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


class MessagesWindow(BoxLayout):
    def __init__(self, messages, **kwargs):
        super(MessagesWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'

        scroll_view = ScrollView()

        box_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)

        self.messages = {message[0]: message[1] for message in messages}

        for message_title in self.messages.keys():
            btn = Button(text=message_title, size_hint_y=None, height=40)
            btn.bind(on_press=self.message_button_pressed)
            box_layout.add_widget(btn)

        scroll_view.add_widget(box_layout)
        self.add_widget(scroll_view)

    def message_button_pressed(self, instance):
        selected_message_text = self.messages.get(instance.text, "Message not found")
        popup = Popup(title=instance.text, content=Label(text=selected_message_text), size_hint=(None, None), size=(300, 200))
        popup.open()


class MessagePage(BoxLayout):
    def __init__(self, db, app, **kwargs):
        super(MessagePage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.db = db
        self.app = app

        self.add_widget(Label(text='Add a Title'))
        self.title_input = TextInput(multiline=True)
        self.add_widget(self.title_input)

        self.add_widget(Label(text='Add a Message'))
        self.message_input = TextInput(multiline=True)
        self.add_widget(self.message_input)

        self.add_message_btn = Button(text='Add Message')
        self.add_message_btn.bind(on_press=self.add_message)
        self.add_widget(self.add_message_btn)

        self.show_messages_btn = Button(text='Show Messages')
        self.show_messages_btn.bind(on_press=self.show_messages_popup)
        self.add_widget(self.show_messages_btn)

        self.messages_label = Label(text='')
        self.add_widget(self.messages_label)

        self.add_back_button()

    def add_message(self, instance):
        title = self.title_input.text
        message = self.message_input.text
        self.db.add_message(title, message)
        self.title_input.text = ''
        self.message_input.text = ''
        self.show_messages(instance)

    def show_messages(self, instance):
        messages = [i[0] + ": " + i[1] for i in self.db.get_messages()]
        self.messages_label.text = '\n'.join(messages)

    def show_messages_popup(self, instance):
        messages = self.db.get_messages()

        messages_window = MessagesWindow(messages)
        popup = Popup(title='Messages', content=messages_window, size_hint=(None, None), size=(400, 400))
        popup.open()

    def add_back_button(self):
        back_btn = Button(text='Back')
        back_btn.bind(on_press=self.app.show_start_page)
        self.add_widget(back_btn)

class MyApp(App):
    def build(self):
        self.db = Database()

        self.root = BoxLayout(orientation='vertical')
        self.login_page = LoginPage(self.db, app=self)
        self.signup_page = SignupPage(self.db, app=self)
        self.message_page = MessagePage(self.db, app=self)
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

    def show_message_page(self):
        self.root.clear_widgets()
        self.root.add_widget(self.message_page)

    def show_start_page(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.start_page)


if __name__ == '__main__':
    MyApp().run()
