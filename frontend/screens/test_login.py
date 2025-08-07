import sys
import os
from kivy.app import App
from kivy.lang import Builder

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

# Мок API
class MockAPI:
    @staticmethod
    def check_user(code):
        print(f"[TEST] Проверка пользователя: {code}")
        return code in ["A12345", "T00001"]

sys.modules['frontend.api'] = MockAPI

# KV-разметка
Builder.load_string('''
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'GreenCity - Вход'
            font_size: 24

        TextInput:
            id: code_input
            hint_text: 'Ваш код (A12345)'
            multiline: False
            font_size: 18
            size_hint_y: None
            height: 50
            input_filter: lambda text, from_undo: text.upper() if len(text) == 1 else (text if text.isdigit() else '')

        Button:
            text: 'Войти'
            size_hint_y: None
            height: 50
            on_press: root.login()
''')

from frontend.screens.login import LoginScreen

class LoginTestApp(App):
    def build(self):
        return LoginScreen(name='login')

if __name__ == '__main__':
    LoginTestApp().run()