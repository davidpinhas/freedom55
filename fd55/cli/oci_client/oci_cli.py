import oci
import json
from prettytable import PrettyTable
import logging
from fd55.utils.oci_config_validator import OciValidator
from fd55.utils.functions import Functions as fn
from fd55.utils.fd55_config import Config
logger = logging.getLogger()
config = Config()


class Oci:
    """ OCI tools """
    logger = None
    identity = None
    user = None
    key_id = None

    def __init__(self, config, identity, user, key_id):
        self.config = config
        self.identity = identity
        self.user = user
        self.key_id = key_id
        self.setup_logger()

    def oci_data_table(object_list, items=None, id=None, **kwargs):
        """ Create OCI data table """
        default_field_names = ['Name', 'State', 'Time Created']
        table = PrettyTable()
        new_data = json.loads(str(object_list.data))
        object_items = new_data
        default_row = []
        if items:
            object_items = new_data['items']
        for obj in object_items:
            data = obj
            if kwargs:
                for key, value in kwargs.items():
                    for inner_key, inner_value in value.items():
                        default_field_names.append(str(inner_key))
                        default_row = [
                            data['display_name'],
                            data['lifecycle_state'],
                            data['time_created']]
                        for ip in data[inner_value]:
                            if ip['is_public']:
                                default_row.append(ip['ip_address'])
            else:
                default_field_names = ['Name', 'State', 'Time Created']
                default_row = [
                    data['display_name'],
                    data['lifecycle_state'],
                    data['time_created']]
            if id:
                default_field_names.append('ID')
                default_row.append(data['id'])
            table.field_names = default_field_names
            table.add_row(default_row)
        print(table)

    def run_init_oci():
        """ Verify OCI init state is ready """
        config = Config()
        config.start_configuration(
            component="OCI",
            key_list=config.oci_key_list)
        if not OciValidator.init_oci():
            config = OciValidator.validate_config_exist()
        elif OciValidator.init_oci():
            config = OciValidator.validate_config_exist()
        else:
            logging.warn(
                f"Something went wrong! Check the config file is valid {config}")
            logging.error(f"Failed to load config, exiting...")
            exit()
        return config

    def encrypt(plaintext):
        """ KMS encrypt """
        Oci.run_init_oci()
        logging.info("Encrypting string with KMS")
        encoded_plaintext = fn.base64_encode(plaintext)
        encrypt_response = OciValidator.set_config_oci_key_client().encrypt(
            encrypt_data_details=oci.key_management.models.EncryptDataDetails(
                plaintext=encoded_plaintext,
                key_id=OciValidator.set_config()["key_id"],
                key_version_id=OciValidator.set_config()["key_version_id"]))
        logging.info(
            f"Encrypted string value - {fn.json_parse(encrypt_response.data)}")
        return fn.json_parse(encrypt_response.data)

    def decrypt(plaintext):
        """ KMS decrypt """
        Oci.run_init_oci()
        logging.info("Decrypting string with KMS")
        decrypt_response = OciValidator.set_config_oci_key_client().decrypt(
            decrypt_data_details=oci.key_management.models.DecryptDataDetails(
                ciphertext=plaintext,
                key_id=OciValidator.set_config()["key_id"],
                key_version_id=OciValidator.set_config()["key_version_id"]))
        data = fn.base64_decode(decrypt_response)
        logging.info(f"Decrypted string - {data}")

    def list_kms_vaults(id=None):
        """ List vaults """
        logging.info("Retrieving vaults data")
        vaults = OciValidator.set_config_oci_kms_vault_client().list_vaults(
            compartment_id=OciValidator.set_config()["tenancy"])
        Oci.oci_data_table(object_list=vaults, id=id)

    def create_vault(name):
        """ Create vault """
        vault_details = OciValidator.set_vault_details(name=name)
        try:
            new_vault = OciValidator.set_config_oci_kms_vault_client(
            ).create_vault(create_vault_details=vault_details)
            data = json.loads(str(new_vault.data))
            logging.info(f"Created vault '{data['display_name']}'")
        except oci.exceptions.ServiceError as e:
            logging.error(f"Failed to create vault with error:\n{e}")

    def delete_vault(vault_id, days=None):
        """ Delete vault """
        try:
            if days:
                if int(days) < 7:
                    logging.error("Not acceptable value for days")
                    logging.error("Can only accept 7 and above")
                    exit()
                else:
                    delete_vault = OciValidator.set_config_oci_kms_vault_client().schedule_vault_deletion(
                        vault_id=vault_id,
                        schedule_vault_deletion_details=OciValidator.set_schedule_vault_deletion(
                            days=days))
            else:
                delete_vault = OciValidator.set_config_oci_kms_vault_client().schedule_vault_deletion(
                    vault_id=vault_id, schedule_vault_deletion_details=OciValidator.set_schedule_vault_deletion())
            data = json.loads(str(delete_vault.data))
            logging.info(
                f"Deleted vault '{data['display_name']}' with ID - {data['id']}")
        except oci.exceptions.ServiceError as e:
            logging.error(f"Failed with message:\n{e}")

    def list_lb(id=None):
        """ List load balancers """
        kwargs = {'Public IP': 'ip_addresses'}
        lb_client = OciValidator.set_lb_client()
        lb_list = lb_client.list_network_load_balancers(
            compartment_id=OciValidator.set_config()["tenancy"])
        Oci.oci_data_table(
            object_list=lb_list,
            items=True,
            id=id,
            kwargs=kwargs)

    def list_lb_nsg(id=None):
        """ List load balancer NSG """
        logging.info(
            f"Listing load balancer network security groups")
        lb_nsg_list = OciValidator.set_virtual_network_client().list_network_security_groups(
            compartment_id=OciValidator.set_config()["tenancy"])
        Oci.oci_data_table(object_list=lb_nsg_list, id=id)

    def list_lb_nsg_rules(id=None):
        """ List load balancer NSG rules """
        logging.info(
            f"Listing load balancer network security groups for ID - {id}")
        lb_nsg_rules_list = OciValidator.set_virtual_network_client(
        ).list_network_security_group_security_rules(network_security_group_id=id)
        object_items = lb_nsg_rules_list.data
        for obj in object_items:
            table = PrettyTable()
            table.field_names = ['Key', 'Value']
            data = json.loads(str(obj))
            for key, value in data.items():
                row = [key, value]
                table.add_row(row)
            print(table)

    def update_lb_nsg_rule(
            id=None,
            rule_id=None,
            protocol=None,
            direction=None,
            description=None,
            destination=None,
            destination_type=None,
            icmp_type=None,
            icmp_code=None,
            is_stateless=None,
            source=None,
            source_type=None,
            tcp_destination_min=None,
            tcp_destination_max=None,
            tcp_source_min=None,
            tcp_source_max=None,
            udp_destination_min=None,
            udp_destination_max=None,
            udp_source_min=None,
            udp_source_max=None):
        """ Update load balancer NSG rule """
        logging.info("Updating load balancer network security group rule")
        core_client = OciValidator.set_virtual_network_client()
        icmp_options = oci.core.models.IcmpOptions(
            type=icmp_type,
            code=icmp_code)
        tcp_destination_range = oci.core.models.PortRange(
            max=int(tcp_destination_max) if tcp_destination_max else None,
            min=int(tcp_destination_min) if tcp_destination_min else None)
        tcp_source_range = oci.core.models.PortRange(
            max=int(tcp_source_max) if tcp_source_max else None,
            min=int(tcp_source_min) if tcp_source_min else None)
        udp_destination_range = oci.core.models.PortRange(
            max=int(udp_destination_max) if udp_destination_max else None,
            min=int(udp_destination_min) if udp_destination_min else None)
        udp_source_range = oci.core.models.PortRange(
            max=int(udp_source_max) if udp_source_max else None,
            min=int(udp_source_min) if udp_source_min else None)
        tcp_options = oci.core.models.TcpOptions(
            destination_port_range=tcp_destination_range)
        if tcp_destination_max and tcp_destination_min and tcp_source_max and tcp_source_min:
            tcp_options = oci.core.models.TcpOptions(
                destination_port_range=tcp_destination_range,
                source_port_range=tcp_source_range)
        udp_options = oci.core.models.UdpOptions(
            destination_port_range=udp_destination_range)
        if udp_destination_range and udp_source_range:
            udp_options = oci.core.models.UdpOptions(
                destination_port_range=udp_destination_range,
                source_port_range=udp_source_range)
        kargs = {
            'direction': direction,
            'id': rule_id,
            'protocol': protocol,
            'description': description,
            'destination': destination,
            'destination_type': destination_type,
            'is_stateless': is_stateless,
            'source': source,
            'source_type': source_type,
        }
        if icmp_type or icmp_code:
            kargs['icmp_options'] = icmp_options
        if tcp_destination_min or tcp_destination_max or tcp_source_min or tcp_source_max:
            kargs['tcp_options'] = tcp_options
        if udp_destination_min or udp_destination_max or udp_source_min or udp_source_max:
            kargs['udp_options'] = udp_options
        logging.debug(f"Provided arguments: {kargs}")

        # https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.90.2/core/update_network_security_group_security_rules.py.html
        new_test = core_client.update_network_security_group_security_rules(
            network_security_group_id=id,
            update_network_security_group_security_rules_details=oci.core.models.UpdateNetworkSecurityGroupSecurityRulesDetails(
                security_rules=[
                    oci.core.models.UpdateSecurityRuleDetails(
                        **kargs)]))
        logging.info(
            f"Successfully updated NSG rule with the following response:\n{new_test.data}")

    #### KMS SECRETS ####

    # def dict_to_secret(dictionary):
    # return
    # base64.b64encode(json.dumps(dictionary).encode('ascii')).decode("ascii")

    # def secret_to_dict(wallet):
    # return
    # json.loads(base64.b64decode(wallet.encode('ascii')).decode('ascii'))

    # # Encode the secret.
    # secret_content_details = Base64SecretContentDetails(
    #     content_type=oci.vault.models.SecretContentDetails.CONTENT_TYPE_BASE64,
    #     stage=oci.vault.models.SecretContentDetails.STAGE_CURRENT,
    #     content=dict_to_secret(plaintext_secret))

    # # Bundle the secret and metadata about it.
    # secrets_details = CreateSecretDetails(
    #         compartment_id=compartment_id,
    #         description = "Data Science service test secret",
    #         secret_content=secret_content_details,
    #         secret_name="DataScienceSecret_{}".format(str(uuid.uuid4())[-6:]),
    #         vault_id=vault_id,
    #         key_id=key_id)

    # # Store secret and wait for the secret to become active.
    # print("Creating secret...", end='')
    # vaults_client_composite = VaultsClientCompositeOperations(VaultsClient(config))
    # secret = vaults_client_composite.create_secret_and_wait_for_state(
    #              create_secret_details=secrets_details,
    #              wait_for_states=[oci.vault.models.Secret.LIFECYCLE_STATE_ACTIVE]).data
    # secret_id = secret.id
    # print('Done')
    # print("Created secret: {}".format(secret_id))

    # # Get secrets list
    # secrets = VaultsClient(config).list_secrets(compartment_id)
    # for secret in secrets.data:
    #     print("Name: {}\nLifecycle State: {}\nOCID: {}\n---".format(
    #         secret.secret_name, secret.lifecycle_state,secret.id))
