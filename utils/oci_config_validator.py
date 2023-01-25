import oci
import logging
import json
from InquirerPy import inquirer
from datetime import datetime, timedelta
from utils.functions import Functions as fn
from utils.fd55_config import Config
logger = logging.getLogger()
cli_config = Config()


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

    def set_lb_client():
        """ Set the OCI load balancer client """
        oci_lb_client = oci.network_load_balancer.NetworkLoadBalancerClient(
            OciValidator.set_config())
        return oci_lb_client

    def set_virtual_network_client():
        """ Set the OCI Virtual Network client """
        oci_virtual_network_client = oci.core.VirtualNetworkClient(
            OciValidator.set_config())
        return oci_virtual_network_client

    def set_lb_nsg_rules_details(security_rules=None):
        """ Set details for load balancer network security group rule update """
        lb_nsg_rules_details = oci.core.models.UpdateNetworkSecurityGroupSecurityRulesDetails(security_rules=security_rules)
        return lb_nsg_rules_details

    def set_security_rule_details(id=None, protocol=None, direction=None, description=None, destination=None, destination_type=None, icmp_type=None, icmp_code=None, is_stateless=None, source=None, source_type=None, tcp_destination_min=None, tcp_destination_max=None, tcp_source_min=None, tcp_source_max=None, udp_destination_min=None, udp_destination_max=None, udp_source_min=None, udp_source_max=None):
        """ Set details for security rule update """
        security_rule = oci.core.models.UpdateSecurityRuleDetails()
        security_rule.id = str(id)
        security_rule.protocol = str(protocol)
        security_rule.direction = str(direction)
        security_rule.description = str(description)
        security_rule.destination = str(destination)
        security_rule.destination_type = str(destination_type)
        security_rule.is_stateless = str(is_stateless)
        security_rule.source = str(source)
        return security_rule

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
        OciValidator.verify_kms_vault_key()
        data = OciValidator.oci_retrieve_service_accounts_keys()
        fn.json_parse(data)
        for i in range(len(data)):
            keys_json = data[int(i)]
            if cli_config.get(section="OCI", option="kms_vault") in str(
                fn.json_parse(
                    keys_json,
                    key='display_name')):
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

    def setup_kms_vault(vault_name=None):
        """ Select KMS vault """
        if vault_name:
            cli_config.create_option(
                section='OCI',
                option='kms_vault',
                value=vault_name)
            logging.info(
                f"Setting up '{vault_name}' as KMS vault in config file")
            return
        vault_list = []
        logging.info("Retrieving active vaults")
        vaults = OciValidator.set_config_oci_kms_vault_client().list_vaults(
            compartment_id=OciValidator.set_config()["tenancy"])
        for vault in vaults.data:
            data = json.loads(str(vault))
            if str(data['lifecycle_state']) != 'ACTIVE':
                logging.debug(f"Vault '{data['display_name']}', is not active")
                logging.debug(
                    f"Vault '{data['display_name']}' state is '{data['lifecycle_state']}'")
                continue
            vault_list.append(data['display_name'])
        result = inquirer.select(
            message="Press enter to choose a KMS vault:",
            choices=vault_list).execute()
        logging.info(f"Setting up vault '{result}' in config file")
        cli_config.create_option(
            section='OCI',
            option='kms_vault',
            value=result)

    def verify_kms_vault_key():
        if not cli_config.get(section="OCI", option="kms_vault"):
            logging.error("No KMS vault configured")
            fn.modify_config_approval(
                f"Do you want to setup KMS vault? Y/n: ")
            OciValidator.setup_kms_vault()

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
        OciValidator.retrieve_oci_service_accounts()
        missing_keys_list = OciValidator.oci_find_missing_keys()
        if missing_keys_list:
            logging.warn(
                f"The OCI configuration is missing the following keys: \n{missing_keys_list}")
            fn.modify_config_approval(
                "Would you like to generate the missing keys? Y/n: ")
            for i in missing_keys_list[::-1]:
                missing_keys_list = OciValidator.oci_find_missing_keys()
                OciValidator.modify_config_file(missing_key=i)
                logging.info(f"Retrieved the key '{i}'")
            logging.info(f"Finished retrieving missing keys")
        else:
            return True
