import subprocess
from cli.functions import Functions as fn
import os
import logging
import platform
import os.path
from os import path
from utils.fd55_config import Config
config = Config()
logger = logging.getLogger()


class Sops:
    """ SOPS tools """

    def __init__(self, config, user):
        self.config = config
        self.user = user

    def find_age_key(key_file):
        """ Locate the public key value """
        logging.debug(
            f"Searching for public key in key.txt file under {key_file} path")
        logging.debug(f"This is key - {key_file}")
        if path.isfile(key_file):
            with open(key_file, "r") as f:
                key_data = f.read()
                logging.debug(f"This is key data - {key_data}")
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
        """ Encrypt file with SOPS using Age """
        logging.info("Encrypting file with SOPS")
        key_id = Sops.find_age_key(f"{config.get('SOPS', 'key_path')}")
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
            logging.error(
                f'Error encrypting file with sops: {proc.stderr.decode()}')
            exit()
        logging.info(f"Finished encrypting {output_file} file")

    def decrypt(input_file, output_file):
        """ Decrypt file with SOPS using Age """
        logging.info("Decrypting file with SOPS")
        cmd = ['sops', '-d', '--output', output_file, input_file]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if proc.returncode != 0:
            logging.error(
                f'Error encrypting file "{input_file}" with sops: {proc.stderr.decode()}')
            exit()
        logging.info(f"Finished encrypting {output_file} file")
