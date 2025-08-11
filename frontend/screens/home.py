from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from frontend.api_client import check_user
from frontend.api_client import add_waste
from frontend.widgets.waste_card import WasteCard  # Добавлен правильный импорт

Builder.load_string('''
<HomeScreen>:
    waste_container: waste_container

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Добавить мусор'
            font_size: 24

        ScrollView:
            BoxLayout:
                id: waste_container
                orientation: 'vertical'
                spacing: 15
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: 'Мой профиль'
            size_hint_y: None
            height: 50
            on_press: root.go_to_profile()
''')


class HomeScreen(Screen):
    user_code = ""
    waste_container = ObjectProperty(None)

    def on_pre_enter(self):
        self.waste_container.clear_widgets()
        wastes = [
            ('lids', 'Пластиковые крышки', '♻️'),
            ('plastic', 'Пластиковые бутылки', '🥤'),
            ('batteries', 'Батарейки', '🔋')
        ]

        for waste in wastes:
            card = WasteCard()
            card.waste_type = waste[0]
            card.title = waste[1]
            card.icon = waste[2]
            card.on_add = self.add_waste
            self.waste_container.add_widget(card)

    def add_waste(self, waste_type, amount):
        result = add_waste(self.user_code, waste_type, amount)
        if result.get('success'):
            print(f"Успешно добавлено: {amount} {waste_type}")
        else:
            print(f"Ошибка: {result.get('error', 'Unknown error')}")

    def go_to_profile(self):
        self.manager.get_screen('profile').user_code = self.user_code
        self.manager.current = 'profile'