import datetime
import os
from kivy.core.image import Texture
from kivy.utils import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import time
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.camera import Camera
from kivy.core.image import Image
from android.permissions import Permission, request_permissions
from android.storage import primary_external_storage_path


__version__ = '0.1.2'
class MenuScreen(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.texture: Texture = None
        self.box_menu = BoxLayout(orientation='vertical')
        self.add_widget(self.box_menu)


class CameraScreen(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name
        date_now = datetime.datetime.now()
        self.year = date_now.strftime("%Y")
        self.mouth = date_now.strftime("%B")
        self.day = date_now.strftime("%d")
        if platform == 'android':
            self.dir_path = primary_external_storage_path()
            self.download_dir_path = os.path.join(self.dir_path, 'Download')
            dcim_dir_path = os.path.join(self.dir_path, 'DCIM')
            self.save_image_path = os.path.join(dcim_dir_path, 'Camera_Images', self.year, self.mouth, self.day)
            if not os.path.exists(self.save_image_path):
                os.makedirs(self.save_image_path, exist_ok=True)
        self.__place_widgets()

    def __place_widgets(self):
        self.box_camera = BoxLayout(orientation='vertical',)
        self.log_box = BoxLayout()
        self.text_log = TextInput()
        self.scroll_view = ScrollView()
        self.button_play = Button(text='Play', on_press=self.capture)
        self.button_save = Button(text='Save foto', on_press=self.save_foto)
        self.add_widget(self.box_camera)
        self.box_camera.add_widget(self.button_play)
        self.box_camera.add_widget(self.button_save)
        self.box_camera.add_widget(self.scroll_view)
        self.scroll_view.add_widget(self.text_log)

    def capture(self, inst):
        camera = Camera(resolution=(640, 480))
        camera.bind(on_texture=self.on_texture)

    def on_texture(self, camera):
        self.texture = camera.texture

    def save_foto(self, button):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        image = Image(self.texture)
        date_dir_path = f'/{self.year}/{self.mouth}'
        image.save(os.path.join(self.save_image_path, "IMG_{}.png".format(timestr)))
        log_name = f'camapp{__version__}.log'
        log_file_path = os.path.join(self.download_dir_path, log_name)
        with open(log_file_path, 'a') as log_file:
            log_file.write('\n'.join('rinat'))
        self.text_log.text = f'Foto saved {self.save_image_path}\n'


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