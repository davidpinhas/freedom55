import json
import base64
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(type.__name__)

def json_parse(json_input):
    """ JSON parser """
    json_data = json.loads(str(json_input))
    logging.info("Running parser")
    if "ciphertext" in json_data:
        jsonData = json_data["ciphertext"]
    else:
        jsonData = json_data["plaintext"]
    logging.info("Parser done")
    return jsonData

def bas64_encode(sample_string):
    """ Base64 encode """
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def bas64_decode(sample_string):
    """ Base64 decode """
    b64decoded_string = base64.b64decode(sample_string + b'==')
    return b64decoded_string