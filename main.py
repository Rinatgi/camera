import os
from kivy.core.image import Texture
from kivy.utils import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.camera import Camera
from kivy.core.image import Image
from android.permissions import Permission, request_permissions


class MenuScreen(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.texture: Texture = None
        self.box_menu = BoxLayout(orientation='vertical')
        self.btn = Button(text='ghbvth')
        self.add_widget(self.box_menu)


class CameraScreen(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name
        if platform == 'android':
            from android.storage import primary_external_storage_path
            dir_path = primary_external_storage_path()
            self.download_dir_path = os.path.join(dir_path, 'Download')
        self.__place_widgets()

    def __place_widgets(self):
        self.box_camera = BoxLayout(orientation='vertical',)
        self.button_play = Button(text='Play', on_press=self.capture)
        self.button_save = Button(text='Save foto', on_press=self.save_foto)
        self.add_widget(self.box_camera)
        self.box_camera.add_widget(self.button_play)
        self.box_camera.add_widget(self.button_save)
        self.text = TextInput()

    def capture(self, inst):
        camera = Camera(resolution=(640, 480))
        camera.bind(on_texture=self.on_texture)

    def on_texture(self, camera):
        self.texture = camera.texture

    def save_foto(self, button):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        image = Image(self.texture)
        image.save(self.download_dir_path + "IMG_{}.png".format(timestr))


class MainScreen(ScreenManager):
    def __init__(self):
        super().__init__()
        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        self.menu_screen = MenuScreen(name='menu')
        self.camera_screen = CameraScreen(name='camera')
        self.button_camera = Button(text='Camera', on_press=lambda x: self.set_screen('camera'))
        self.button_setting = Button(text='Setting', on_press=lambda x: self.set_screen('setting'))
        self.button_back_menu = Button(text='Back menu', on_press=lambda x: self.set_screen('menu'))

    def __place_widgets(self):
        self.add_widget(self.menu_screen)
        self.add_widget(self.camera_screen)
        self.menu_screen.box_menu.add_widget(self.button_camera)
        self.menu_screen.box_menu.add_widget(self.button_setting)
        self.camera_screen.box_camera.add_widget(self.button_back_menu)

    def set_screen(self, name_screen):
        self.current = name_screen


class MainApp(App):

    def build(self):
        request_permissions(
            [
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
            ]
        )
        return MainScreen()


MainApp().run()