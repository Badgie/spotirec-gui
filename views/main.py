import PySimpleGUI as sg
from .models import SpotirecButton
from .static import THEME, EXIT
from .customize import CustomizeView
from .device import DeviceView
from .playlist import PlaylistView


class MainView:
    WIDTH = 220
    HEIGHT = 400

    def __init__(self):
        sg.theme_background_color(THEME['BACKGROUND'])
        sg.theme_element_background_color(THEME['BACKGROUND'])
        sg.theme_text_element_background_color(THEME['BACKGROUND'])
        sg.theme_text_color(THEME['TEXT'])
        sg.theme_input_background_color(THEME['INPUT'])
        sg.theme_button_color(THEME['BUTTON'])
        sg.theme_progress_bar_color(THEME['PROGRESS'])
        sg.theme_border_width(THEME['BORDER'])
        sg.theme_slider_border_width(THEME['SLIDER_DEPTH'])
        sg.theme_progress_bar_border_width(THEME['PROGRESS_DEPTH'])
        sg.theme_slider_color(THEME['SCROLL'])
        sg.theme_element_text_color(THEME['TEXT'])
        sg.theme_input_text_color(THEME['TEXT_INPUT'])

        header_img = sg.Image(filename='assets/img/header/header-200x67.png',
                              size=(self.WIDTH, self.HEIGHT // 4))

        playlist_btn = SpotirecButton('Playlists')
        device_btn = SpotirecButton('Devices')
        config_btn = SpotirecButton('Customize')
        recom_btn = SpotirecButton('Recommend')
        exit_btn = SpotirecButton('Exit', button='red')

        layout = [[header_img],
                  [playlist_btn],
                  [device_btn],
                  [config_btn],
                  [recom_btn],
                  [exit_btn]]

        window = sg.Window('Spotirec', layout=layout, size=(self.WIDTH, self.HEIGHT),
                           element_justification='center')

        while True:
            event, values = window.read()
            if event == 'Playlists':
                PlaylistView()
            elif event == 'Devices':
                DeviceView()
            elif event == 'Customize':
                CustomizeView()
            elif event == 'Recommend':
                continue
            if event in EXIT:
                break

        window.close()
