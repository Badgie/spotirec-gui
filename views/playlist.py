import PySimpleGUI as sg
from spotirec import conf
from models import SpotirecButton
from static import EXIT


class PlaylistView:
    WIDTH = 400
    HEIGHT = 600

    def __init__(self):
        save_btn = SpotirecButton('Save')
        cancel_btn = SpotirecButton('Cancel')

        layout = [[save_btn, cancel_btn]]
        window = sg.Window('Playlists', layout=layout, size=(self.WIDTH, self.HEIGHT),
                           element_justification='center')
        while True:
            event, values = window.read()
            print(event)
            if event in EXIT:
                break

        window.close()
