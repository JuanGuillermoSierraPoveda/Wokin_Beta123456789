from tkinter.ttk import Label
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from basedatos import registrar_usuario, verificar_usuario
from kivymd.toast import toast

import basedatos

global qin,qfin,map
qin=""
qfin=""
map=""

class SplashScreen(Screen):
    pass

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if verificar_usuario(username, password):
            MDApp.get_running_app().user_name = username
            self.manager.current = "home"
        else:
            self.ids.msg.text = "Credenciales inválidas"

class SignupScreen(Screen):
    def signup(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if registrar_usuario(username, password):
            self.ids.msg.text = "Registro exitoso"
        else:
            self.ids.msg.text = "Usuario ya existe"

class HomeScreen(Screen):
    current_screen = StringProperty("home")
    def cambiar_contenido(self, screen_name):
        #print("cambio",screen_name)
        self.manager.current = screen_name

class SearchScreen(Screen):
    current_screen = StringProperty("search")
    def cambiar_contenido(self, screen_name):
        self.manager.current = screen_name

class MapScreen(Screen):
    current_screen = StringProperty("map")
    
    def cambiar_contenido(self, screen_name):
        print("BBBBBB")
        self.manager.current = screen_name

    def poner_estado(self, estado):
        def poner_estado(self, estado):
            print("AAAAAAAAAA", estado)
            self.ids.q0.text = f"Pressed {estado}"


class MapSelScreen(Screen):
    current_screen = StringProperty("mapsel")
    def cambiar_contenido(self, screen_name):
        self.manager.current = screen_name

class ProfileScreen(Screen):
    current_screen = StringProperty("perfil")
    profile_image_source = StringProperty("icons/edit user.png")
    def cambiar_contenido(self, screen_name):
        self.manager.current = screen_name
    def open_gallery(self):
        filechooser.open_file(on_selection=self.selected_image, filters=[
            "*.png", "*.jpg", "*.jpeg", "*.gif"
        ])
    def selected_image(self, selection):
        if selection:
            image_path = selection[0]
            self.profile_image_source = image_path
            print(f"Nueva imagen de perfil seleccionada: {image_path}")

class SettingsScreen(Screen):
    current_screen = StringProperty("settings")
    def cambiar_contenido(self, screen_name):
        self.manager.current = screen_name

class FavoritesScreen(Screen):
    current_screen = StringProperty("favorites")
    def cambiar_contenido(self, screen_name):
        self.manager.current = screen_name

class InformacionPersonalScreen(Screen):
    is_editing_username = BooleanProperty(False)
    is_editing_password = BooleanProperty(False)
    
    # Propiedades para almacenar los datos del usuario para mostrarlos
    display_username = StringProperty("")

    def on_enter(self, *args):
        """Carga los datos del usuario cuando se accede a esta pantalla."""
        self.load_user_data()
        # Asegurarse de que los campos estén en modo solo lectura al entrar
        self.ids.username_input.readonly = True
        self.ids.password_input.readonly = True
        self.ids.edit_username_button.text = "Editar"
        self.ids.edit_password_button.text = "Editar"
        self.is_editing_username = False
        self.is_editing_password = False

    def load_user_data(self):
        # Obtiene el nombre de usuario actual desde la instancia de la aplicación
        current_username = MDApp.get_running_app().user_name
        
        # Carga los datos desde la base de datos
        user_data = basedatos.obtener_usuario_por_username(current_username)

        if user_data:
            self.display_username = user_data["username"]
            
            # Asigna los valores a los TextInput y Labels en el KV
            self.ids.username_input.text = self.display_username
        else:
            toast("Error: No se pudo cargar la información del usuario.")
            # Si no se encuentra el usuario, quizás redirigir o mostrar un mensaje
            self.ids.username_input.text = "Usuario no encontrado"

    def toggle_edit_mode(self, field):
        if field == 'username':
            self.is_editing_username = not self.is_editing_username
            self.ids.username_input.readonly = not self.is_editing_username
            self.ids.edit_username_button.text = "Guardar" if self.is_editing_username else "Editar"
            if self.is_editing_username:
                self.ids.username_input.focus = True # Pone el foco en el campo
            else:
                self.save_changes('username') # Guarda cambios al volver a "Editar"
        
        elif field == 'password':
            self.is_editing_password = not self.is_editing_password
            self.ids.password_input.readonly = not self.is_editing_password
            self.ids.password_input.password = not self.is_editing_password # Muestra/oculta al editar
            self.ids.edit_password_button.text = "Guardar" if self.is_editing_password else "Editar"
            if self.is_editing_password:
                self.ids.password_input.text = "" # Borra para que el usuario escriba la nueva
                self.ids.password_input.focus = True
            else:
                self.save_changes('password') # Guarda cambios al volver a "Editar"

    def save_changes(self, field):
        current_username_app = MDApp.get_running_app().user_name # Nombre de usuario original del login

        if field == 'username':
            new_username = self.ids.username_input.text.strip()
            if new_username and new_username != current_username_app:
                if basedatos.actualizar_username(current_username_app, new_username):
                    MDApp.get_running_app().user_name = new_username # Actualiza el nombre en la aplicación global
                    self.display_username = new_username # Actualiza la propiedad de la pantalla
                    toast("Nombre de usuario actualizado.")
                else:
                    toast("Error: Ese nombre de usuario ya existe o no se pudo actualizar.")
                    self.ids.username_input.text = current_username_app # Revierte al original
            elif not new_username:
                toast("El nombre de usuario no puede estar vacío.")
                self.ids.username_input.text = current_username_app # Revierte al original
        
        elif field == 'password':
            new_password = self.ids.password_input.text.strip()
            if new_password and new_password != "********": # "********" es el valor por defecto si no se edita
                if basedatos.actualizar_password(current_username_app, new_password):
                    toast("Contraseña actualizada.")
                else:
                    toast("Error: No se pudo actualizar la contraseña.")
            elif not new_password:
                toast("La contraseña no puede estar vacía.")
            self.ids.password_input.text = "********" # Vuelve a ocultar la contraseña

# ... (El resto de tu clase WindowManager)

class WindowManager(ScreenManager):
    pass

class Wokin(MDApp):
    user_name = StringProperty("Invitado")
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        Window.size = (360, 640)

        Builder.load_file('inicio.kv')
        Builder.load_file('signup.kv')
        Builder.load_file('login.kv')
        Builder.load_file('home.kv')
        Builder.load_file('search.kv')
        Builder.load_file('perfil.kv')
        Builder.load_file('settings.kv')
        Builder.load_file('favorites.kv')
        Builder.load_file('informacion personal.kv')
        Builder.load_file('map.kv')
        Builder.load_file('mapsel.kv')

        sm = WindowManager()
        sm.add_widget(SplashScreen(name='splash'))
        Clock.schedule_once(lambda dt: self.change_screen(sm), 2)
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(ProfileScreen(name="perfil"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(FavoritesScreen(name="favorites"))
        sm.add_widget(InformacionPersonalScreen(name="informacion_personal"))
        sm.add_widget(MapScreen(name='map'))
        sm.add_widget(MapScreen(name='mapsel'))
        return sm

    def change_screen(self, sm):
        sm.current = 'signup'

if __name__ == '__main__':
    Wokin().run()
