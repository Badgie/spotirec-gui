import PySimpleGUI as sg
from spotirec import conf
from .models import SpotirecButton
from .static import EXIT


class DeviceView:
    WIDTH = 400
    HEIGHT = 600

    def __init__(self):
        save_btn = SpotirecButton('Save')
        cancel_btn = SpotirecButton('Cancel')

        layout = [[save_btn, cancel_btn]]
        window = sg.Window('Devices', layout=layout, size=(self.WIDTH, self.HEIGHT),
                           element_justification='center')
        while True:
            event, values = window.read()
            if event in EXIT:
                break

        window.close()
