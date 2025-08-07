import sys
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)


# Мок API
class MockAPI:
    @staticmethod
    def add_waste(user_code, waste_type, amount):
        print(f"[TEST] Добавлено: {amount} {waste_type} для {user_code}")
        return {'success': True, 'newCount': amount}

    @staticmethod
    def get_user_stats(code):
        return {
            'name': 'Тестовый Ученик',
            'class': '10А',
            'waste': {'lids': 5, 'plastic': 3, 'batteries': 2},
            'total_points': 31
        }


sys.modules['frontend.api'] = MockAPI

# KV-разметка
Builder.load_string('''
<WasteCard>:
    orientation: 'vertical'
    spacing: 10
    size_hint_y: None
    height: 120
    padding: 10

    BoxLayout:
        size_hint_y: None
        height: 30
        spacing: 10

        Label:
            text: root.title
            font_size: 18
            halign: 'left'
            size_hint_x: 0.7

        Label:
            text: root.icon
            font_size: 20

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10

        Button:
            text: '-'
            size_hint_x: 0.2
            on_press: root.amount = max(0, root.amount - 1)

        Label:
            text: str(root.amount)
            font_size: 24
            size_hint_x: 0.6
            halign: 'center'

        Button:
            text: '+'
            size_hint_x: 0.2
            on_press: root.amount += 1

    Button:
        text: 'Добавить'
        size_hint_y: None
        height: 40
        on_press: root.add_waste()
''')

from frontend.screens.home import HomeScreen
from frontend.widgets.waste_card import WasteCard


class HomeTestApp(App):
    def build(self):
        sm = ScreenManager()
        home = HomeScreen(name='home')
        home.user_code = "T00001"  # Тестовый код пользователя
        sm.add_widget(home)
        return sm


if __name__ == '__main__':
    HomeTestApp().run()