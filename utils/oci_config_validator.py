import oci
import logging
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

    def set_config():
        config = OciValidator.validate_config_exist()
        return config

    def set_config_service_endpoint():
        service_endpoint = OciValidator.set_config()["service_endpoint"]
        return service_endpoint

    def set_config_service_endpoint_mgmt():
        service_endpoint_mgmt = OciValidator.set_config()[
            "service_endpoint_mgmt"]
        return service_endpoint_mgmt

    def oci_key_list():
        keys_list = ["user", "fingerprint", "tenancy", "region",
                     "key_file", "key_id", "key_version_id", "service_endpoint", "service_endpoint_mgmt"]
        return keys_list

    def set_config_oci_key_client():
        oci_key_client = oci.key_management.KmsCryptoClient(
            OciValidator.set_config(), OciValidator.set_config_service_endpoint())
        return oci_key_client

    def retrieve_oci_key_id():
        """ retrieve OCI key id  """
        key_management_client = oci.key_management.KmsManagementClient(
            OciValidator.set_config(), OciValidator.set_config_service_endpoint_mgmt())
        keys = key_management_client.list_keys(
            OciValidator.set_config()["tenancy"])
        keys_json = keys.data[0]
        logging.debug(f"Key ID - {fn.json_parse(keys_json, key='id')}")
        return str(fn.json_parse(keys_json, key='id'))

    def retrieve_oci_key_version_id():
        key_id = OciValidator.retrieve_oci_key_id()
        key_management_client = oci.key_management.KmsManagementClient(
            OciValidator.set_config(), OciValidator.set_config_service_endpoint_mgmt())
        keys = key_management_client.list_key_versions(key_id)
        keys_json = keys.data[0]
        logging.debug(
            f"Key ID versions - {fn.json_parse(keys_json, key='id')}")
        return fn.json_parse(keys_json, key='id')

    def retrieve_oci_service_accounts(MGMT_VALUE=None, CRYPTO_VALUE=None):
        data = OciValidator.oci_retrieve_service_accounts_keys()
        fn.json_parse(data)
        for i in range(len(data)):
            keys_json = data[int(i)]
            if str(fn.json_parse(keys_json, key='lifecycle_state')) == "DELETED":
                logging.debug(f"Deleted asset {data[i]}. Skipping")
                continue
            else:
                if fn.json_parse(keys_json, key='management_endpoint'):
                    MGMT_VALUE = True
                    logging.debug(
                        f"this is management_endpoint - {fn.json_parse(keys_json, key='management_endpoint')}")
                if fn.json_parse(keys_json, key='crypto_endpoint'):
                    logging.debug(
                        f"this is crypto_endpoint - {fn.json_parse(keys_json, key='crypto_endpoint')}")
                    CRYPTO_VALUE = True
                return [fn.json_parse(keys_json, key='management_endpoint'), fn.json_parse(keys_json, key='crypto_endpoint')]

    def oci_retrieve_service_accounts_keys():
        key_management_client = oci.key_management.KmsVaultClient(
            OciValidator.set_config())
        keys = key_management_client.list_vaults(
            OciValidator.set_config()["tenancy"])
        data = keys.data
        return data

    def oci_find_missing_keys():
        logging.debug("Searching for missing keys")
        config = OciValidator.validate_config_exist()
        key_list = OciValidator.oci_key_list()
        new_list = []
        for i in key_list:
            if i not in config:
                new_list.append(i)
        return new_list

    def modify_config_approval():
        logging.warn(f"Required keys are missing from the config file")
        user_approval = input(
            f"Would you like to generate the missing keys? Y/N: ")
        if user_approval:
            return True
        else:
            return False

    def add_key_to_config(key_name, key_value):
        config_path = fn.find_config_file()
        with open(config_path, 'a') as f:
            f.write(f"\n{key_name}={key_value}")

    def modify_config_file(missing_key=None, added_keys=[], auto_approve=False):
        config = OciValidator.validate_config_exist()
        if missing_key not in config:
            if missing_key.startswith("service_endpoint"):
                func = getattr(OciValidator, f"retrieve_oci_service_accounts")
                if missing_key.endswith("mgmt"):
                    OciValidator.add_key_to_config(missing_key, func()[0])
                else:
                    OciValidator.add_key_to_config(missing_key, func()[1])
            else:
                func = getattr(OciValidator, f"retrieve_oci_{missing_key}")
                OciValidator.add_key_to_config(missing_key, func())
        else:
            logging.info(f"Key {missing_key} was added")

    def init_oci(config=None):
        OciValidator.validate_config_exist()
        missing_keys_list = OciValidator.oci_find_missing_keys()
        if missing_keys_list:
            OciValidator.modify_config_approval()
            for i in missing_keys_list[::-1]:
                missing_keys_list = OciValidator.oci_find_missing_keys()
                OciValidator.modify_config_file(missing_key=i)
        else:
            return True
