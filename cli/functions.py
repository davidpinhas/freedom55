import json
import base64
import logging
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
