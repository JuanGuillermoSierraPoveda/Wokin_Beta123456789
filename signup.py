from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock

class SplashScreen(Screen):
    pass

class TestApp(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class SignupScreen(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Window.size = (360, 640)

        Builder.load_file('inicio.kv')
        Builder.load_file('signup.kv')

        sm = WindowManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(TestApp(name='signup'))

        Clock.schedule_once(lambda dt: self.change_screen(sm), 2)
        return sm

    def change_screen(self, sm):
        sm.current = 'signup'

if __name__ == '__main__':
    SignupScreen().run()
