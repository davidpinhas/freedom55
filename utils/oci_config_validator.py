import oci
import logging
from pathlib import Path
from cli.functions import Functions as fn

logging.basicConfig(encoding='utf-8', level=logging.INFO)


class OciValidator:
    """ OCI config validator """

    def validate_config_exist():
        oci_conf_path = fn.find_config_file()
        try:
            config = oci.config.from_file(f"{oci_conf_path}", "DEFAULT")
        except:
            logging.error(
                "There was an issue with the OCI config, verify the file exists")
            exit()
        return config

    def validate_key(config):
        modify_confing_file_flag = False
        """ Validate config keys """
        keys_list = ["user", "fingerprint", "tenancy", "region",
                     "key_file", "key_id", "key_version_id", "service_endpoint", "service_endpoint_mgmt"]
        logging.info("Validating OCI config file")
        for i in keys_list:
            if i not in config:
                logging.error(f" Value '{i}' is incorrect or missing")
                user_approval = input(f"Would you like to generate the key {i}? Y/N\n")
                if user_approval == "y" or user_approval == "Y":
                    modify_confing_file_flag=True
                    values = (i, modify_confing_file_flag)
                    return values
                elif user_approval == "n" or user_approval == "N":
                    logging.info("Exiting.")
                    exit()
                else:
                    logging.error("Incorrect input, user 'y' or 'Y'")
                    exit()
            else:
                pass

        logging.info("All config keys exist")
