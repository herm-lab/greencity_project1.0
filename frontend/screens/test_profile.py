import sys
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.core.window import Window

# Установка размера окна
Window.size = (400, 700)

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)


# Мок API
class MockAPI:
    @staticmethod
    def get_user_stats(code):
        return {
            'name': 'Тестовый Пользователь',
            'classInfo': '11А',  # Используем тот же ключ, что и в основном коде
            'waste': {
                'lids': 10,
                'plastic': 5,
                'batteries': 2
            },
            'total_points': 10 * 5 + 5 * 3 + 2 * 10  # 50 + 15 + 20 = 85
        }


sys.modules['frontend.api'] = MockAPI


# Тестовый экран home
class TestHomeScreen(Screen):
    user_code = StringProperty("A12345")


# KV разметка
kv = '''
<ProfileScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Профиль'
            font_size: 24

        Label:
            id: user_info
            font_size: 18

        BoxLayout:
            orientation: 'vertical'
            spacing: 10


            Label:
                id: stats_info
                font_size: 16

        Button:
            text: 'Закрыть'
            size_hint_y: None
            height: 50
            on_press: app.stop()

<TestHomeScreen>:
    Label:
        text: 'Тестовый экран Home\\nКод: ' + root.user_code
        font_size: 24
'''

Builder.load_string(kv)

from frontend.screens.profile import ProfileScreen


class ProfileTestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TestHomeScreen(name='home'))

        profile = ProfileScreen(name='profile')
        sm.add_widget(profile)

        sm.current = 'profile'
        return sm


if __name__ == '__main__':
    ProfileTestApp().run()