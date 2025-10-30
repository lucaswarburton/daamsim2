import configparser
from pathlib import Path

class Configuration:
    _instance = None
    _config_file_path = Path.cwd() / "config.ini"

    def __init__(self):
        print(Configuration._config_file_path)
        self.parseConfig()

    def get_instance():
        if Configuration._instance == None:
            Configuration._instance =  Configuration()
        return Configuration._instance

    def parseConfig(self):
        parser = configparser.ConfigParser()
        parser.read(Configuration._config_file_path)

        disable_ui = parser['Settings']['ui_disabled']
        disable_ui = disable_ui.lower()

        self.disable_ui = disable_ui == 'true' or   disable_ui == 't' or disable_ui == 'y' or disable_ui == 'yes'
        self.default_file_path = parser['Settings']['default_file_path']

        #Set default intruder speed array
        min_speed =  int(parser['DEFAULTS']['min_intruder_speed'])
        max_speed = int(parser['DEFAULTS']['max_intruder_speed'])
        speed_interval = int(parser['DEFAULTS']['intruder_speed_interval'])

        self.d_intuder_speed_array = list(range(min_speed, max_speed, speed_interval))
        self.d_intuder_speed_array += [max_speed]
