import oci
import json
from prettytable import PrettyTable
import logging
from utils.oci_config_validator import OciValidator
from InquirerPy import inquirer
from cli.functions import Functions as fn
from utils.fd55_config import Config
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

    def run_init_oci():
        config = Config()
        config.start_configuration(
            component="OCI",
            key_list=config.oci_key_list)
        """ Verify OCI init state is ready """
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
        table = PrettyTable()
        vaults = OciValidator.set_config_oci_kms_vault_client().list_vaults(
            compartment_id=OciValidator.set_config()["tenancy"])
        for obj in vaults.data:
            data = json.loads(str(obj))
            if id:
                table.field_names = ['Name', 'State', 'ID', 'Time Created']
                row = [
                    data['display_name'],
                    data['lifecycle_state'],
                    data['id'],
                    data['time_created']]
            else:
                table.field_names = ['Name', 'State', 'Time Created']
                row = [
                    data['display_name'],
                    data['lifecycle_state'],
                    data['time_created']]
            table.add_row(row)
        print(table)

    def setup_kms_vault():
        """ Select KMS vgault """
        vault_list = []
        logging.info("Retrieving active vaults")
        vaults = OciValidator.set_config_oci_kms_vault_client().list_vaults(
            compartment_id=OciValidator.set_config()["tenancy"])
        for vault in vaults.data:
            data = json.loads(str(vault))
            if str(data['lifecycle_state']) != 'ACTIVE':
                logging.debug(f"Vault '{data['display_name']}', is not active")
                logging.debug(f"Vault '{data['display_name']}' state is '{data['lifecycle_state']}'")
                continue
            vault_list.append(data['display_name'])
        result = inquirer.select(message="Pick a KMS vault:", choices=vault_list).execute()
        logging.info(f"Setting up vault '{result}' in config file")
        config.create_option(section='OCI', option='kms_vault', value=result)

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
