import json
import base64
import logging
import os
logger = logging.getLogger()


class Functions:
    """ CLI functions """
    def set_logger(verbosity):
        logger = logging.basicConfig(
            level=verbosity,
            format='%(asctime)s|%(levelname)s|%(message)s')
        return logger

    def file_exists(filename):
        return os.path.exists(filename)

    def modify_config_approval(string: str):
        """ Request user approval to modify file """
        user_approval = input(
            f"{string}")
        if user_approval:
            return True
        else:
            return False

    def delete_file(file_path):
        if Functions.file_exists(f"{str(file_path)}"):
            user_input = Functions.modify_config_approval(
                "Config file already exists, would you like to replace it? Y/n: ")
            if user_input:
                os.remove(f"{str(file_path)}")
                logging.info(f"Deleted config file {file_path}")

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
        if key is not None:
            logging.debug(f"Parsing with key {key}")
            json_output = json_data[key]
        logging.debug("Parser done")
        return json_output

    def open_json_file(json_file):
        try:
            with open(json_file, 'r') as f:
                return json.load(f)
        except BaseException:
            logging.error("JSON file might be corrupted or doesn't exist")
            exit()

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
