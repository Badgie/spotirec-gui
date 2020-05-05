import PySimpleGUI as sg
from typing import Union
from .models import SpotirecButton
from .static import EXIT, SCHEMES
from .device import DeviceView
from spotirec.spotirec import TUNE_ATTR, TUNE_PREFIX
from spotirec import conf, log, api, spotirec, oauth2


class CustomizeView:
    WIDTH = 400
    HEIGHT = 600
    LOGGER = log.Log()
    CONF = conf.Config()
    CONF.set_logger(LOGGER)
    API = api.API()
    API.set_logger(LOGGER)
    API.set_conf(CONF)
    OAUTH = oauth2.SpotifyOAuth()
    OAUTH.set_conf(CONF)
    OAUTH.set_logger(LOGGER)
    OAUTH.set_api(API)
    spotirec.logger = LOGGER
    spotirec.conf = CONF
    spotirec.api = API
    spotirec.sp_oauth = OAUTH
    spotirec.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {spotirec.get_token()}'}

    def __init__(self):
        self.rows = 1

        scheme = sg.Combo(SCHEMES, default_value='Top genres', enable_events=True, key='scheme',
                          size=(self.WIDTH, 0))
        self.scheme_frame = sg.Frame('Recommendation scheme', [[scheme]])

        self.custom_seeds = [[sg.Combo([], enable_events=True, key=f'seed{x}',
                                       size=(self.WIDTH, 10), visible=False)] for x in range(5)]
        self.custom_seeds_input = [[sg.InputText('', enable_events=True, key=f'text_seed{x}',
                                                 visible=False)] for x in range(5)]
        self.seed_box = sg.Frame('Seeds', [*self.custom_seeds, *self.custom_seeds_input],
                                 visible=False)

        limit = sg.InputText('100', enable_events=True, key='limit', size=(self.WIDTH, 0))
        self.limit_frame = sg.Frame('Amount of tracks', [[limit]])

        preserve = sg.Checkbox('', enable_events=True, key='preserve', size=(self.WIDTH, 0))
        self.preserve_frame = sg.Frame('Create new playlist', [[preserve]])

        auto_play = sg.Checkbox('', enable_events=True, key='play', size=(self.WIDTH, 0))
        self.auto_play_frame = sg.Frame('Auto play', [[auto_play]])

        # should probably be last
        tuning_prefix = sg.Combo(TUNE_PREFIX, enable_events=True, key='tuning_prefix0')
        tuning_attr = sg.Combo(list(TUNE_ATTR['int'].keys()) + list(TUNE_ATTR['float'].keys()),
                               enable_events=True, key='tuning_attr0')
        tuning_val = sg.InputText('', enable_events=True, key='tuning_val0')
        tuning_add_btn = SpotirecButton('', 'circle-add', dims='16x16', key='add_tuning_row')
        self.tuning_frame = sg.Frame('Tuning', [[tuning_prefix, tuning_attr, tuning_val]])

        # only visible if auto play is checked
        device = sg.Combo(list(self.CONF.get_devices().keys()),
                          enable_events=True, key='device', size=(self.WIDTH, 0))
        self.device_add = SpotirecButton('', 'circle-add', dims='16x16', key='add_device',
                                         visible=False)
        self.device_frame = sg.Frame('Select device', [[device]], visible=False)

        save_btn = SpotirecButton('Save')
        cancel_btn = SpotirecButton('Cancel', button='red')

        self.layout = [[self.scheme_frame],
                       [self.seed_box],
                       [self.limit_frame],
                       [self.preserve_frame],
                       [self.auto_play_frame],
                       [self.device_add],
                       [self.device_frame],
                       [tuning_add_btn],
                       [self.tuning_frame],
                       [save_btn, cancel_btn]]

        self.window = self._create_window()
        self.window.finalize()
        while True:
            event, values = self.window.read()
            print(event)
            if event == 'add_tuning_row':
                self._add_tuning_row()
                self.window.refresh()
            if event == 'add_device':
                DeviceView()
            if event == 'play':
                self.device_frame.update(visible=values['play'])
                self.device_add.update(visible=values['play'])
                self.window.refresh()
            if event == 'scheme':
                self._update_scheme_opts(values['scheme'])
            if event in EXIT:
                break
            if event == 'Save':
                self._validate(values)
            print(self.window.size)
            print(self.scheme_frame.get_size())

        self.window.close()

    def _create_window(self) -> sg.FlexForm:
        return sg.FlexForm('Customize recommendations', layout=self.layout,
                           size=(self.WIDTH, self.HEIGHT))

    def _add_tuning_row(self):
        tune_attrs = list(TUNE_ATTR['int'].keys()) + list(TUNE_ATTR['float'].keys())
        if len(tune_attrs) == self.rows:
            return
        tuning_prefix = sg.Combo(TUNE_PREFIX, enable_events=True, key=f'tuning_prefix{self.rows}')
        tuning_attr = sg.Combo(list(TUNE_ATTR['int'].keys()) + list(TUNE_ATTR['float'].keys()),
                               enable_events=True, key=f'tuning_attr{self.rows}')
        tuning_val = sg.InputText('', enable_events=True, key=f'tuning_val{self.rows}')
        self.window.extend_layout(self.tuning_frame, [[tuning_prefix, tuning_attr, tuning_val]])
        self.rows += 1

    def _update_scheme_opts(self, scheme):
        self.__clear_scheme_opts()
        if 'Custom' in scheme:
            if scheme == 'Custom':
                for x in self.custom_seeds_input:
                    for y in x:
                        y.update(visible=True)
                self.seed_box.update(visible=True)
                return
            for x in self.custom_seeds:
                data = None
                if 'top genres' in scheme:
                    data = spotirec.get_user_top_genres()
                elif 'top tracks' in scheme:
                    data = {f'{x["name"]} -> {x["artists"][0]["name"]}': x['uri']
                            for x in self.API.get_top_list('tracks', 50, spotirec.headers)['items']}
                elif 'top artists' in scheme:
                    data = {x['name']: x['uri']
                            for x in self.API.get_top_list('artists', 50,
                                                           spotirec.headers)['items']}
                elif 'saved tracks' in scheme:
                    data = {f'{x["track"]["name"]} -> {x["track"]["artists"][0]["name"]}':
                            x['track']['uri'] for x in self.API.get_saved_tracks(spotirec.headers,
                                                                                 limit=50)['items']}
                elif 'genre seeds' in scheme:
                    data = self.API.get_genre_seeds(spotirec.headers)['genres']
                for y in x:
                    y.update(visible=True, values=[''] + self.__data(data))
                self.seed_box.update(visible=True)
        self.window.refresh()

    def _validate(self, values: dict):
        pass

    def __clear_scheme_opts(self):
        for x in range(len(self.seed_box.Rows)):
            for y in self.seed_box.Rows[x]:
                y.update(visible=False)
        self.seed_box.update(visible=False)
        self.window.refresh()

    def __data(self, data: Union[list, dict]):
        if type(data) == dict:
            return list(data.keys())
        return data
