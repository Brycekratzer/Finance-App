import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label

# Inherits screen widget. Corresponds to the screens defined in Kivy Language

class MainScreen(Screen): 
    pass

class AnotherScreen(Screen):
    pass

class MyApp(App):
    def build(self): # where 
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AnotherScreen(name='another'))
        return sm

if __name__ == '__main__':
    MyApp().run()
