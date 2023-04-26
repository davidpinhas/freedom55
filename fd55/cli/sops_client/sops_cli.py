import subprocess
import logging
from os import path, environ
from fd55.utils.fd55_config import Config
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
        if path.isfile(key_file):
            with open(key_file, "r") as f:
                key_data = f.read()
                logging.debug(f"Key data:\n{key_data}")
            lines = key_data.split("\n")
            for line in lines:
                if line.startswith("# public key:"):
                    return line.split(": ")[1]
                elif not line.startswith("# public key:"):
                    pass
                else:
                    logging.error(
                        "public key is not present inside key.txt file")
                    exit()
        else:
            logging.error(
                f"There seems to be an issue with the key.txt file, please check if it exists under {key_file}")
            exit()

    def verify_key_file(key_file):
        """ Verify Age key file """
        key_id = key_file
        if not key_file:
            key_id = Sops.find_age_key(f"{config.get('SOPS', 'key_file')}")
        else:
            key_id = Sops.find_age_key(key_file)
            environ['SOPS_AGE_KEY_FILE'] = f"{key_file}"
        if not key_id:
            logging.error("Key path is required")
            exit()
        return key_id

    def encrypt(input_file, output_file, encrypted_regex=None, key_file=None):
        """ Encrypt file with SOPS using Age """
        logging.info("Encrypting file with SOPS")
        key_id = Sops.verify_key_file(key_file=key_file)
        if not key_file:
            key_id = Sops.find_age_key(f"{config.get('SOPS', 'key_file')}")
        logging.debug(f"Using key ID - {key_id}")
        if not encrypted_regex:
            cmd = ['sops', '--encrypt', '--age', key_id,
                   '--output', output_file, input_file]
        else:
            logging.info(f"Using regex: {encrypted_regex}")
            cmd = ['sops', '--encrypt', '--age', key_id, '--encrypted-regex',
                   f'{encrypted_regex}', '--output', output_file, input_file]
        logging.debug(f"Running the command - {cmd}")
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if proc.returncode != 0:
            logging.error(
                f'Error encrypting file {input_file}: {proc.stderr.decode()}')
            exit()
        logging.info(f"Finished encrypting {output_file} file")

    def decrypt(input_file, output_file, key_file=None):
        """ Decrypt file with SOPS using Age """
        logging.info("Decrypting file with SOPS")
        key_id = Sops.verify_key_file(key_file=key_file)
        if not key_file:
            key_id = Sops.find_age_key(f"{config.get('SOPS', 'key_file')}")
        logging.debug(f"Using key ID - {key_id}")
        cmd = [
            'sops',
            '-d',
            '--age',
            key_id,
            '--output',
            output_file,
            input_file]
        logging.debug(f"Running the command - {cmd}")
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if proc.returncode != 0:
            logging.error(
                f'Error decrypting file "{input_file}" with sops: {proc.stderr.decode()}')
            exit()
        logging.info(f"Finished decrypting {output_file} file")
