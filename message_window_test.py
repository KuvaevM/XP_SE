import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


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

        self.popup = None

    def message_button_pressed(self, instance):
        selected_message_text = self.messages.get(instance.text, "Message not found")
        self.popup = Popup(title=instance.text, content=Label(text=selected_message_text), size_hint=(None, None), size=(300, 200))
        self.popup.open()


class TestMessagesWindow(GraphicUnitTest):
    def setUp(self):
        super(TestMessagesWindow, self).setUp()
        self.sample_messages = [("Title 1", "Message 1"), ("Title 2", "Message 2")]
        self.messages_window = MessagesWindow(self.sample_messages)

    def test_message_button_pressed(self):
        mock_button = type('Button', (), {'text': 'Title 1'})()

        self.messages_window.message_button_pressed(mock_button)

        self.assertTrue(self.messages_window.popup.title == 'Title 1')
        self.assertTrue(self.messages_window.popup.content.text == 'Message 1')


if __name__ == '__main__':
    unittest.main()
