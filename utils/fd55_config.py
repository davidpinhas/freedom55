import logging
import configparser
import os
import platform
from cli.functions import Functions as fn
logger = logging.getLogger()
component_list = ["OCI", "SOPS", "ARGOCD", "TERRAFORM"]

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
            logging.warn("Configuration directory doesn't exist")
            logging.info(f"Creating configuration directory under {config_dir}")
            os.makedirs(config_dir)
        return config_dir

    def validate_config_section(self):
        """ Validate the configuration file """
        for component in component_list:
            if not self.config.has_section(component):
                return False
            return True

    def validate_config_option(self, key_list, component):
        """ Validate the configuration file """
        logging.info("Validating fd55 config file")
        logging.debug(f"fd55 config file is located under {self._get_config_dir()}/config.ini")
        if not self.config.has_section(component):
            return False
        else:
            for option in key_list:
                if not self.config.has_option(component, option):
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
        if not config.validate_config_option(key_list=fn.oci_key_list ,component="OCI"):
            if config.start_configuration(component="OCI", key_list=fn.oci_key_list):
                print('Configuration complete!')
            else:
                print('Configuration failed.')
        else:
            print('Configuration is valid.')