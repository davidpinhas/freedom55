import oci
import json
from prettytable import PrettyTable
import logging
from utils.oci_config_validator import OciValidator
from cli.functions import Functions as fn
from utils.fd55_config import Config
logger = logging.getLogger()

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
        Oci.run_init_oci()

    def run_init_oci():
        config = Config()
        config.start_configuration(component="OCI", key_list=config.oci_key_list)
        """ Verify OCI init state is ready """
        if not OciValidator.init_oci():
            config = OciValidator.validate_config_exist()
        elif OciValidator.init_oci():
            config = OciValidator.validate_config_exist()
        else:
            logging.warn(f"Something went wrong! This is the config - {config}")
            logging.error(f"Failed to load config, exiting...")
            exit()
        return config

    def encrypt(plaintext):
        """ KMS encrypt """
        logging.info("Encrypting string with KMS")
        encoded_plaintext = fn.base64_encode(plaintext)
        encrypt_response = OciValidator.set_config_oci_key_client().encrypt(
            encrypt_data_details=oci.key_management.models.EncryptDataDetails(
                plaintext=encoded_plaintext,
                key_id=OciValidator.set_config()["key_id"],
                key_version_id=OciValidator.set_config()["key_version_id"]))
        logging.info(
            f"Encrypted string value - {fn.json_parse(encrypt_response.data)}")

    def decrypt(plaintext):
        """ KMS decrypt """
        logging.info("Decrypting string with KMS")
        decrypt_response = OciValidator.set_config_oci_key_client().decrypt(
            decrypt_data_details=oci.key_management.models.DecryptDataDetails(
                ciphertext=plaintext,
                key_id=OciValidator.set_config()["key_id"],
                key_version_id=OciValidator.set_config()["key_version_id"]))
        data = fn.base64_decode(decrypt_response)
        logging.info(f"Decrypted string - {data}")

    def list_kms_vaults():
        """ List vaults """
        logging.info("Retrieving vaults data")
        table = PrettyTable()
        table.field_names = ['Name', 'State', 'Time Created']
        vaults = OciValidator.set_config_oci_kms_vault_client().list_vaults(
            compartment_id=OciValidator.set_config()["tenancy"])
        for obj in vaults.data:
            data = json.loads(str(obj))
            row = [data['display_name'], data['lifecycle_state'], data['time_created']]
            table.add_row(row)
        print(table)
        return vaults
    
    def create_vault():
        pass

    def delete_vault():
        pass
        
    #### KMS SECRETS ####

    # def dict_to_secret(dictionary):
    #     return base64.b64encode(json.dumps(dictionary).encode('ascii')).decode("ascii")

    # def secret_to_dict(wallet):
    #     return json.loads(base64.b64decode(wallet.encode('ascii')).decode('ascii'))

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