from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from frontend.api import create_user  # Или используйте относительный импорт, как было ранее

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


class AdminScreen(Screen):
    def create_account(self):
        name = self.ids.name_input.text.strip()
        class_info = self.ids.class_input.text.strip()

        if not name or not class_info:
            self.show_message("Заполните все поля")
            return

        response = create_user(name, class_info)

        if 'code' in response:
            code = response['code']
            self.show_message(
                f"Аккаунт создан!\nКод ученика: {code}\n"
                "Сообщите этот код ученику!",
                title="Успех"
            )
            self.ids.name_input.text = ""
            self.ids.class_input.text = ""
        else:
            self.show_message("Ошибка при создании аккаунта")

    def show_message(self, message, title="Сообщение"):
        content = Label(text=message, padding=10)
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5)  # Убедитесь, что здесь нет лишних символов
        )
        popup.open()