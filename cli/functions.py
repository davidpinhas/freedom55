import json
import base64
import logging
import shutil
import os
import datetime
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(type.__name__)


class Functions:
    """ CLI functions """

    def json_parse(json_input, key=None):
        """ JSON parser """
        logging.debug("Running parser")
        json_data = json.loads(str(json_input))
        if key is None:
            logging.debug(f"Parsing without key")
            if "ciphertext" in json_data:
                jsonData = json_data["ciphertext"]
                json_output = jsonData
            elif "plaintext" in json_data:
                jsonData = json_data["plaintext"]
                json_output = jsonData
            else:
                json_output = json_data
        if key!=None:
            logging.debug(f"Parsing with key {key}")
            json_output = json_data[key]
        logging.debug("Parser done")
        return json_output

    def base64_encode(sample_string):
        """ Base64 encode """
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def base64_decode(sample_string):
        """ Base64 decode """
        data = str(base64.b64decode(Functions.json_parse(sample_string.data)))
        return data.strip("b'").strip("'")

    def find_config_file():
        """ Find OCI config file path """
        config_file_name = ".oci/config"
        home_dir = os.path.expanduser("~")
        config_file_path = os.path.join(home_dir, config_file_name)
        if os.path.exists(config_file_path):
            logging.debug("The config file was found at: " + config_file_path)
        else:
            logging.error("The OCI config file was not found.")
            exit()
        return config_file_path

    def oci_config_backup():
        """ Backup OCI config file to conf_backup dir """
        logging.info("Backing up OCI config file")
        file_name = "config"
        file_dir = Functions.find_config_file().strip('config')
        backup_dir = f"{file_dir}conf_backup"
        if not os.path.exists(backup_dir):
            logging.warn(f"conf_backup directory doesn't exist, created the dir under {backup_dir}")
            os.makedirs(backup_dir)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file_name = file_name + "_" + timestamp
        copy_file_name = os.path.join(backup_dir, backup_file_name)
        os.rename(os.path.join(file_dir, file_name), os.path.join(backup_dir, backup_file_name))
        shutil.copy(copy_file_name, os.path.join(file_dir, file_name))
        logging.info(f"Backup finished successfully. The backup file is located at {copy_file_name}")