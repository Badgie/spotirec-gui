import PySimpleGUI as sg
from tkinter import Tk
from tk_html_widgets import HTMLLabel
from requests import get
from spotirec import oauth2, log

spotirec_colors = {'BACKGROUND': '#1C2F39',
                   'TEXT': '#91A0A0',
                   'INPUT': '#4D4D4D',
                   'TEXT_INPUT': '#00D482',
                   'SCROLL': '#91A0A0',
                   'BUTTON': ('#FFFFFF', '#00D482'),
                   'PROGRESS': '#00D482',
                   'BORDER': 1,
                   'SLIDER_DEPTH': 0,
                   'PROGRESS_DEPTH': 0}


# STUCK ON FINDING HTML EMBEDDING
# tkhtml and tkinterhtml arent maintained
# tk_html_widgets doesnt support css/js
# cefpython3 embeds a whole browser and is fucking massive
class AuthView:

    def __init__(self, url):
        self.url = url
        content = get(self.url).content.decode('utf-8')
        print(content)
        root = Tk()
        html = HTMLLabel(root, html=content)
        html.pack(fill='both', expand=True)
        html.fit_height()
        root.mainloop()


auth = oauth2.SpotifyOAuth()
auth.PORT = 8000
auth.set_logger(log.Log())
view = AuthView(auth.get_authorize_url())

print(view.url)
