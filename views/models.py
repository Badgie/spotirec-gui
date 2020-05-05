from PySimpleGUI import Button
from .static import THEME


class SpotirecButton(Button):

    def __init__(self, text: str, button: str = 'green', dims='150x40', key=None,
                 button_color=(THEME['BACKGROUND'], THEME['BACKGROUND']),
                 border_width=0, font=('', 13), visible=True):
        super(SpotirecButton, self).__init__(
            text, image_filename=f'assets/img/elems/buttons/button-{button}-{dims}.png',
            border_width=border_width, button_color=button_color, font=font, key=key,
            visible=visible)
