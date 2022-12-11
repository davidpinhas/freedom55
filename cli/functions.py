import json
import base64
import logging
import os
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
        config_file_name = ".oci/config"
        home_dir = os.path.expanduser("~")
        config_file_path = os.path.join(home_dir, config_file_name)
        if os.path.exists(config_file_path):
            logging.debug("The config file was found at: " + config_file_path)
        else:
            logging.error("The OCI config file was not found.")
            exit()
        return config_file_path
