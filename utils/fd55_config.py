import logging
import configparser
import os
import platform

logger = logging.getLogger()

class Config:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_path = os.path.join(self.config_dir, 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def _get_config_dir(self):
        """ Get configuration directory """
        if platform.system() == 'Windows':
            config_dir = os.path.join(os.environ['USERPROFILE'], '.fd55')
        else:
            config_dir = os.path.join(os.path.expanduser('~'), '.fd55')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return config_dir

    def validate_config(self):
        """ Validate the configuration file """
        if not self.config.has_section('section'):
            return False
        if not self.config.has_option('section', 'option'):
            return False
        return True

    def start_configuration(self, component=None, key_list=None):
        """ Prompt the user to configure the application """
        logging.info(f"Setting up config file in {self.config_path}")
        self.config.add_section(component)
        for key in key_list:
            value = input(f'Enter the value for {key}: ')
            self.config.set(component, key, value)
            with open(self.config_path, 'w') as config_file:
                self.config.write(config_file)
        return True

    def run_config_validation(config):
        if not config.validate_config():
            if config.start_configuration():
                print('Configuration complete!')
            else:
                print('Configuration failed.')
        else:
            print('Configuration is valid.')