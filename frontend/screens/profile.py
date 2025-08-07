from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_string('''
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
                text: 'Статистика:'
                font_size: 18

            Label:
                id: stats_info

        Button:
            text: 'Назад'
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'home'
''')


class ProfileScreen(Screen):
    def on_pre_enter(self):
        stats = self.get_user_stats()
        if 'error' in stats:
            self.show_error(stats['error'])
            return

        self.ids.user_info.text = f"{stats['name']}, {stats['classInfo']}"

        stats_text = []
        for waste_type, count in stats['waste'].items():
            stats_text.append(f"{waste_type}: {count} шт")
        stats_text.append(f"\nВсего баллов: {stats['total_points']}")

        self.ids.stats_info.text = '\n'.join(stats_text)

    def get_user_stats(self):
        #Из home
        user_code = self.manager.get_screen('home').user_code
        from frontend.api import get_user_stats
        return get_user_stats(user_code)

    def show_error(self, message):
        Popup(
            title='Ошибка',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        ).open()