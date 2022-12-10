import oci
import logging
from pathlib import Path
logging.basicConfig(encoding='utf-8', level=logging.INFO)

oci_conf_path = Path('~/.oci/config')


class OciValidator:
    """ OCI config validator """

    def validate_config_exist():
        try:
            config = oci.config.from_file(f"{oci_conf_path}", "DEFAULT")
        except:
            logging.error(
                "There was an issue with the OCI config, verify the file exists")
            exit()
        return config

    def validate_key(config):
        """ Validate config keys """
        keys_list = ["user", "fingerprint", "tenancy", "region",
                     "key_file", "key_id", "key_version_id", "service_endpoint"]
        logging.info("Validating OCI config file")
        for i in keys_list:
            if i not in config:
                logging.error(f" Value '{i}' is incorrect or missing")
                exit()
            else:
                pass

        logging.info("All config keys exist")
