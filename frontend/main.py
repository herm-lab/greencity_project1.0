import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Добавляем корневую папку в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Теперь можно использовать абсолютные импорты
from frontend.screens.login import LoginScreen
from frontend.screens.home import HomeScreen
from frontend.screens.profile import ProfileScreen
from frontend.screens.admin import AdminScreen

class GreenCityApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == '__main__':
    GreenCityApp().run()