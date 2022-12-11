import oci
import logging
from utils.oci_config_validator import OciValidator
from cli.functions import Functions as fn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(type.__name__)


class OciConfigHelper:
    """ OCI config helper """
    config = OciValidator.validate_config_exist()
    service_endpoint = config["service_endpoint"]
    service_endpoint_mgmt = config["service_endpoint_mgmt"]

    def __init__(self):
        self.setup_logger()

    def retrieve_oci_vault_key_id():
        key_management_client = oci.key_management.KmsManagementClient(
            OciConfigHelper.config, OciConfigHelper.service_endpoint_mgmt)
        keys = key_management_client.list_keys(
            OciConfigHelper.config["tenancy"])
        keys_json = keys.data[0]
        logging.info(f"Key ID - {fn.json_parse(keys_json, key='id')}")
        return str(fn.json_parse(keys_json, key='id'))

    def retrieve_oci_vault_key_id_versions():
        key_id = OciConfigHelper.retrieve_oci_vault_key_id()
        key_management_client = oci.key_management.KmsManagementClient(
            OciConfigHelper.config, OciConfigHelper.service_endpoint_mgmt)
        keys = key_management_client.list_key_versions(key_id)
        keys_json = keys.data[0]
        logging.info(f"Key ID versions - {fn.json_parse(keys_json, key='id')}")
        return fn.json_parse(keys_json, key='id')

    def retrieve_oci_service_accounts():
        key_management_client = oci.key_management.KmsVaultClient(
            OciConfigHelper.config)
        keys = key_management_client.list_vaults(
            OciConfigHelper.config["tenancy"])
        MGMT_VALUE = None
        CRYPTO_VALUE = None
        data = keys.data
        fn.json_parse(data)
        for i in range(len(keys.data)):
            keys_json = keys.data[int(i)]
            if str(fn.json_parse(keys_json, key='lifecycle_state')) == "DELETED":
                logging.debug(f"Deleted asset {keys.data[i]}. Skipping")
                continue
            else:
                if fn.json_parse(keys_json, key='management_endpoint') and MGMT_VALUE is None:
                    MGMT_VALUE = True
                    logging.info(
                        f"this is management_endpoint - {fn.json_parse(keys_json, key='management_endpoint')}")
                if fn.json_parse(keys_json, key='crypto_endpoint') and CRYPTO_VALUE is None:
                    logging.info(
                        f"this is crypto_endpoint - {fn.json_parse(keys_json, key='crypto_endpoint')}")
                    CRYPTO_VALUE = True

    def setup_config_file(invalid_key):
        logging.info(f"Updating config file")
        exit()
        # TO-DO:
        # Set a backup of ~/.oci/config file with timestamp
        # Append invalid_key with its value to config file
        # loop over each invalid_key and set all required keys
