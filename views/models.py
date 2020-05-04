from PySimpleGUI import Button
from static import THEME


class SpotirecButton(Button):

    def __init__(self, text: str, button_color=(THEME['BACKGROUND'], THEME['BACKGROUND']),
                 button_path='img/elems/buttons/button-150x40.png', border_width=0, font=('', 13)):
        super(SpotirecButton, self).__init__(text, image_filename=button_path,
                                             border_width=border_width, button_color=button_color,
                                             font=font)
