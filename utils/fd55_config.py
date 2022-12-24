import logging
import configparser
import os
import platform
import inquirer
import shutil
import datetime
from cli.functions import Functions as fn
logger = logging.getLogger()
component_list = ["OCI", "SOPS", "ARGOCD", "TERRAFORM"]

class Config:
    oci_key_list = ["user", "fingerprint", "tenancy", "region", "key_file"]
    argo_key_list = ["url", "api_token"]
    sops_key_list = []
    tf_key_list = []

    def __init__(self):
        self.config_dir = self.get_config_dir()
        self.config_path = os.path.join(self.config_dir, 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def get(self, section, option):
        return self.config.get(section, option)

    def get_section(self, section):
        return self.config.options(section)

    def create_option(self, section, option, value):
        self.config.read(self.config_path)
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

    def get_config_dir(self):
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

    def config_backup():
        """ Backup OCI config file to conf_backup dir """
        file_dir = Config().config_path.strip('config.ini')
        backup_dir = f"{file_dir}config_backup"
        if not os.path.exists(backup_dir):
            logging.warn(f"conf_backup directory doesn't exist, created the dir under {backup_dir}")
            os.makedirs(backup_dir)
        if os.path.exists(Config().config_path):
            logging.info("Backing up OCI config file")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_file_name = "config" + "_" + timestamp + ".ini"
            copy_file_name = os.path.join(backup_dir, backup_file_name)
            os.rename(os.path.join(file_dir, "config.ini"), os.path.join(backup_dir, backup_file_name))
            shutil.copy(copy_file_name, os.path.join(file_dir, "config"))
            logging.info(f"Backup finished successfully. The backup file is located at {copy_file_name}")
        else:
            logging.info("No config file was found")
            pass

    def select_components_menu():
        """ Prompt the user to select one or more components from a list """
        config = Config()
        prompt = [
              inquirer.Checkbox('components',
                    message="Select integrations to configure?",
                    choices=component_list,
                    ),
        ]
        selected_options = inquirer.prompt(prompt)
        Config.config_backup()
        fn.delete_file(f"{config.get_config_dir()}/config.ini")
        return selected_options['components']

    def validate_config_section(self, component):
        """ Validate the configuration file """
        if not self.config.has_section(component):
            return False
        return True

    def validate_config_option(self, component, key_list):
        """ Validate the configuration file """
        logging.debug("Validating fd55 config file")
        logging.debug(f"fd55 config file is located under {self.get_config_dir()}/config.ini")
        if not self.validate_config_section(component):
            return False
        else:
            for option in key_list:
                if not self.config.has_option(component, option):
                    return False
        return True

    def start_configuration(self, component, key_list):
        """ Prompt the user to configure the application """
        logging.debug(f"Modifying config file in {self.config_path}")
        if not self.config.has_section(component):
            self.config.add_section(component)
            for key in key_list:
                value = input(f'Enter the value for {key}: ')
                self.config.set(component, key, value)
                with open(self.config_path, 'w') as config_file:
                    self.config.write(config_file)
        else:
            return True
        return True
                        
    def run_config_validation(config):
        selected_items = Config.select_components_menu()
        config = Config()
        for component in selected_items:
            logging.info(f"Setting up the {component} integration")
            if component == "OCI":
                if not config.validate_config_option(component, key_list=config.oci_key_list):
                    if config.start_configuration(component=component, key_list=config.oci_key_list):
                        pass
            if component == "ARGOCD":
                if not config.validate_config_option(component, key_list=config.argo_key_list):
                    if config.start_configuration(component=component, key_list=config.argo_key_list):
                        pass
            if component == "SOPS":
                if not config.validate_config_option(component, key_list=config.sops_key_list):
                    if config.start_configuration(component=component, key_list=config.sops_key_list):
                        pass
            if component == "TERRAFORM":
                if not config.validate_config_option(component, key_list=config.tf_key_list):
                    if config.start_configuration(component=component, key_list=config.tf_key_list):
                        pass
                else:
                    logging.error('Configuration failed.')
                    exit()