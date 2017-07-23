import os

from ConfigParser import ConfigParser

from .exceptions import WorldifyConfigException


class WorldifyConfig(object):
    def __init__(self):
        self._config_path = os.path.expanduser("~/.worldify")
        self.conf = ConfigParser()
        self.conf.read(self._config_path)
        self._check_config_contents()
        self._create_config_objects()

    def _check_config_exsists(self):
        if not os.path.exists(self._config_path):
            raise WorldifyConfigException("No config file found at {0}".format(self._config_path))
        return True

    def _check_config_contents(self):
        expected_config = {
            "twitter": ['customer_key', 'customer_secret', 'access_key', 'access_secret'],
            "recptiviti": ['api_key', 'api_secret'],
            "spotify": ['user_id', 'user_oath', 'client_id', 'client_secret']
        }
        for key in expected_config:
            if not self.conf.has_section(key):
                raise WorldifyConfigException("Could not find the {} section in the worldify "
                                              "config file.".format(key))
            for option in expected_config[key]:
                if not self.conf.has_option(key, option):
                    raise WorldifyConfigException("Could not find the {0}.{1} option in the "
                                                  "worldify config file".format(key, option))

    def _create_config_objects(self):
        self.twitter = {item[0]: item[1] for item in self.conf.items("twitter")}
        self.recptiviti = {item[0]: item[1] for item in self.conf.items("recptiviti")}
        self.spotify = {item[0]: item[1] for item in self.conf.items("spotify")}
