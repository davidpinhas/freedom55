import subprocess
from cli.functions import Functions as fn
import os
import logging
import platform
import os.path
from os import path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(type.__name__)


class Sops:
    """ SOPS tools """

    def __init__(self, config, user):
        self.config = config
        self.user = user

    def find_age_key_file():
        logging.debug("Locating Age key.txt file")
        operating_system = platform.system()
        if operating_system == "Windows":
            key_file = os.environ["APPDATA"] + "\key.txt"
        elif operating_system == "Linux":
            key_file = os.path.expanduser("~/.sops/key.txt")
        elif operating_system == "Darwin":
            key_file = os.path.expanduser("~/.sops/key.txt")
        else:
            key_file = None
            logging.error("The age key.txt is not present")
            exit()
        return key_file

    def find_age_key(key_file):
        logging.debug(
            f"Searching for public key in key.txt file under {key_file} path")
        print(f"This is key {key_file}")
        if path.isfile(key_file):
            with open(key_file, "r") as f:
                key_data = f.read()
                print(f"This is key data - {key_data}")
            lines = key_data.split("\n")
            for line in lines:
                if line.startswith("# public key:"):
                    return line.split(": ")[1]
                elif not line.startswith("# public key:"):
                    pass
                else:
                    logging.error("public key is not present inside key.txt file")
                    exit()
        else:
            logging.error(f"There seems to be an issue with the key.txt file, please check if it exists under {key_file}")
            exit()

    def encrypt(input_file, output_file, encrypted_regex=None):
        logging.info("Encrypting file with SOPS")
        key_id = Sops.find_age_key(Sops.find_age_key_file())
        if not encrypted_regex:
            cmd = ['sops', '--encrypt', '--age', key_id,
                   '--output', output_file, input_file]
        else:
            cmd = ['sops', '--encrypt', '--age', key_id, '--encrypted-regex',
                   f'{encrypted_regex}', '--output', output_file, input_file]
        logging.debug(f"Running the command - {cmd}")
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise Exception(
                f'Error encrypting file with sops: {proc.stderr.decode()}')
        logging.info(f"Finished encrypting {output_file} file")

    def decrypt(input_file, output_file):
        logging.info("Decrypting file with SOPS")
        cmd = ['sops', '-d', '--output', output_file, input_file]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise Exception(
                f'Error decrypting file with sops: {proc.stderr.decode()}')
        logging.info(f"Finished encrypting {output_file} file")
