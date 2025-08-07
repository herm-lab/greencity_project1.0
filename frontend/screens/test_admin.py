import sys
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# Настройка путей для корректного импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.append(project_root)

# Мок API для тестирования
class MockAPI:
    @staticmethod
    def create_user(name, class_info):
        print(f"[TEST] Создан пользователь: {name} ({class_info})")
        return {'code': 'T55555', 'success': True}

# Подменяем настоящий API
sys.modules['frontend.api'] = MockAPI

# Загрузка KV-разметки экрана администратора
Builder.load_string('''
<AdminScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Админ-панель'
            font_size: 24
            size_hint_y: None
            height: 50

        TextInput:
            id: name_input
            hint_text: 'Имя ученика'
            size_hint_y: None
            height: 50

        TextInput:
            id: class_input
            hint_text: 'Класс/группа'
            size_hint_y: None
            height: 50

        Button:
            text: 'Создать аккаунт'
            size_hint_y: None
            height: 50
            on_press: root.create_account()

        Button:
            text: 'Назад'
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'home'
''')

# Импорт экрана после настройки окружения
from frontend.screens.admin import AdminScreen

class AdminTestApp(App):
    def build(self):
        # Создаем ScreenManager с тестовым экраном
        sm = ScreenManager()
        sm.add_widget(AdminScreen(name='admin'))
        return sm

    def on_start(self):
        # Автоматическое тестирование при запуске (опционально)
        admin_screen = self.root.get_screen('admin')
        admin_screen.ids.name_input.text = "Тестовый Ученик"
        admin_screen.ids.class_input.text = "10А"
        print("Авто-тест: Попробуйте нажать 'Создать аккаунт'")

if __name__ == '__main__':
    AdminTestApp().run()