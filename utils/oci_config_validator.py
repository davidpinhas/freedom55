import oci
import logging
from datetime import datetime, timedelta
from cli.functions import Functions as fn
from utils.fd55_config import Config
logger = logging.getLogger()


class OciValidator:
    """ OCI config validator """
    def validate_config_exist():
        """ Validate OCI config file exists """
        oci_conf_path = Config().config_path
        try:
            config = oci.config.from_file(f"{oci_conf_path}", "OCI")
        except BaseException:
            logging.error(
                "An error occurred while attempting to read the OCI configuration file")
            logging.warn(
                "Verify that the file exists and contains the correct keys")
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
        keys_list = [
            "user",
            "fingerprint",
            "tenancy",
            "region",
            "key_file",
            "key_id",
            "key_version_id",
            "service_endpoint",
            "service_endpoint_mgmt"]
        return keys_list

    def set_config_oci_key_client():
        """ Set the OCI KMS crypto client """
        oci_key_client = oci.key_management.KmsCryptoClient(
            OciValidator.set_config(), OciValidator.set_config_service_endpoint())
        return oci_key_client

    def set_config_oci_kms_vault_client():
        """ Set the OCI KMS vault client """
        oci_kms_vault_client = oci.key_management.KmsVaultClient(
            OciValidator.set_config())
        return oci_kms_vault_client

    def set_vault_details(name=None):
        """ Set details for vault creation """
        vault_details = oci.key_management.models.CreateVaultDetails(
            compartment_id=OciValidator.set_config()["tenancy"],
            display_name=name,
            vault_type="DEFAULT")
        return vault_details

    def set_schedule_vault_deletion(days=None):
        """ Set deletion details for vault deletion """
        if not days:
            logging.warn(f"No argument was provided for days")
            logging.info(
                f"Scheduling deletion to the default setting of 30 days from today")
            schedule_vault_deletion = oci.key_management.models.ScheduleVaultDeletionDetails()
        else:
            current_date = datetime.now()
            new_date = current_date + timedelta(days=int(days))
            logging.info(f"Scheduling vault deletion to date: {new_date}")
            schedule_vault_deletion = oci.key_management.models.ScheduleVaultDeletionDetails(
                time_of_deletion=new_date)
        return schedule_vault_deletion

    def retrieve_oci_key_id():
        """ Retrieve OCI key id """
        key_management_client = oci.key_management.KmsManagementClient(
            OciValidator.set_config(), OciValidator.set_config_service_endpoint_mgmt())
        keys = key_management_client.list_keys(
            OciValidator.set_config()["tenancy"])
        if not keys.data:
            logging.error("No keys found. Check KMS vault is up and running.")
            exit()
        keys_json = keys.data[0]
        logging.debug(f"Key ID - {fn.json_parse(keys_json, key='id')}")
        return str(fn.json_parse(keys_json, key='id'))

    def retrieve_oci_key_version_id():
        """ Retrieve OCI key version id """
        key_id = OciValidator.retrieve_oci_key_id()
        key_management_client = oci.key_management.KmsManagementClient(
            OciValidator.set_config(), OciValidator.set_config_service_endpoint_mgmt())
        keys = key_management_client.list_key_versions(key_id)
        keys_json = keys.data[0]
        logging.debug(
            f"Key ID versions - {fn.json_parse(keys_json, key='id')}")
        return fn.json_parse(keys_json, key='id')

    def retrieve_oci_service_accounts():
        """ Retrieve OCI crypto_endpoint and management_endpoint """
        data = OciValidator.oci_retrieve_service_accounts_keys()
        fn.json_parse(data)
        for i in range(len(data)):
            keys_json = data[int(i)]
            if "DEL" in str(
                fn.json_parse(
                    keys_json,
                    key='lifecycle_state')).upper():
                logging.debug(f"Deleted asset:\n{data[i]}.")
                logging.debug("Skipping")
                continue
            else:
                if fn.json_parse(keys_json, key='management_endpoint'):
                    logging.debug(
                        f"located management_endpoint key - {fn.json_parse(keys_json, key='management_endpoint')}")
                if fn.json_parse(keys_json, key='crypto_endpoint'):
                    logging.debug(
                        f"located crypto_endpoint key - {fn.json_parse(keys_json, key='crypto_endpoint')}")
                return [
                    fn.json_parse(
                        keys_json, key='management_endpoint'), fn.json_parse(
                        keys_json, key='crypto_endpoint')]

    def oci_retrieve_service_accounts_keys():
        """ Retrieve a list of all vaults """
        key_management_client = oci.key_management.KmsVaultClient(
            OciValidator.set_config())
        keys = key_management_client.list_vaults(
            OciValidator.set_config()["tenancy"])
        data = keys.data
        return data

    def oci_find_missing_keys():
        """ Find missing keys from OCI config file """
        logging.debug("Searching for missing keys")
        config = Config()
        key_list = [
            "user",
            "fingerprint",
            "tenancy",
            "region",
            "key_file",
            "key_id",
            "key_version_id",
            "service_endpoint",
            "service_endpoint_mgmt"]
        config_key_list = config.get_section("OCI")
        logging.debug(
            f'Keys configured in OCI config section - {config.get_section("OCI")}')
        new_list = []
        for i in key_list:
            if i not in config_key_list:
                logging.debug(f"Missing key - {i}")
                new_list.append(i)
        logging.debug(f"Found missing keys - {new_list}")
        return new_list

    def modify_config_file(missing_key=None):
        """ Modify OCI Config file """
        config = Config()
        config_keys = config.get_section("OCI")
        config.start_configuration(
            component="OCI",
            key_list=OciValidator.oci_find_missing_keys())
        if missing_key not in config_keys:
            if missing_key.startswith("service_endpoint"):
                func = getattr(OciValidator, f"retrieve_oci_service_accounts")
                if missing_key.endswith("mgmt"):
                    config.create_option("OCI", missing_key, func()[0])
                else:
                    config.create_option("OCI", missing_key, func()[1])
            else:
                func = getattr(OciValidator, f"retrieve_oci_{missing_key}")
                config.create_option("OCI", missing_key, func())
        else:
            logging.info(f"Key {missing_key} was added")

    def init_oci(config=None):
        """ Initialize the OCI config file """
        OciValidator.validate_config_exist()
        missing_keys_list = OciValidator.oci_find_missing_keys()
        if missing_keys_list:
            logging.warn(
                f"The OCI configuration is missing the following keys: \n{missing_keys_list}")
            fn.modify_config_approval(
                "Would you like to generate the missing keys? Y/N: ")
            for i in missing_keys_list[::-1]:
                missing_keys_list = OciValidator.oci_find_missing_keys()
                OciValidator.modify_config_file(missing_key=i)
                logging.info(f"Retrieved the key '{i}'")
        else:
            return True
