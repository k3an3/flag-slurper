import getpass
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent


class Config(ConfigParser):
    instance = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    @classmethod
    def load(cls, extra: Optional[str] = None):
        conf = cls()
        conffiles = [
            str(ROOT / 'default.ini'),
            str((Path('~') / '.flagrc').expanduser()),
        ]
        if extra:
            conffiles.append(extra)
        conf.read(conffiles)

        cls.instance = conf
        return conf

    @staticmethod
    def get_instance():
        if not Config.instance:
            Config.load()
        return Config.instance

    def cond_set(self, section, option, value):
        if value is not None:
            self[section][option] = value

    @property
    def api_url(self):
        return '{}/api/{}'.format(self['iscore']['url'], self['iscore']['api_version'])

    @property
    def user(self):
        from .utils import get_user
        if not self._user:
            self._user = get_user()
        return self._user

    def prompt_creds(self):
        if 'api_token' not in self['iscore'] or not self['iscore']['api_token']:
            print('Enter your IScorE API Token (leave blank to use your credentials)')
            self['iscore']['api_token'] = input('> ')

        if not self['iscore']['api_token'] and not hasattr(self, 'credentials'):
            print('Please login using your IScorE credentials')
            username = input('Username: ')
            password = getpass.getpass()
            self.credentials = (username, password)

    def request_extras(self):
        """
        Get extra requests configuration, specifically about authentication.

        Example:
        >>> extras = config.request_extras()
        >>> requests.get(url, **extras)
        """
        conf = {}
        self.prompt_creds()
        if self.has_option('iscore', 'api_token'):
            conf['headers'] = {
                'Authorization': 'Token {}'.format(self['iscore']['api_token']),
            }
        if hasattr(self, 'credentials'):
            conf['auth'] = self.credentials
        return conf