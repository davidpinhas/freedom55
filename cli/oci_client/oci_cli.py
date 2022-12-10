import oci
import json
import click
import base64
import logging
from oci import exceptions
from utils.oci_config_validator import OciValidator
from cli.functions import Functions as fn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(type.__name__)


class Oci:
    """ OCI tools """
    logger = None
    identity = None
    user = None
    key_id = None
    config = OciValidator.validate_config_exist()
    OciValidator.validate_key(config)
    service_endpoint = config["service_endpoint"]
    service_endpoint_mgmt = config["service_endpoint_mgmt"]
    oci_key_client = oci.key_management.KmsCryptoClient(
        config, service_endpoint)

    def __init__(self, config, identity, user, key_id):
        self.config = config
        self.identity = identity
        self.user = user
        self.key_id = key_id
        self.setup_logger()

    def encrypt(plaintext):
        """ KMS encrypt """
        logging.info("Encrypting string with KMS")
        encoded_plaintext = fn.base64_encode(plaintext)
        encrypt_response = Oci.oci_key_client.encrypt(
            encrypt_data_details=oci.key_management.models.EncryptDataDetails(
                plaintext=encoded_plaintext,
                key_id=Oci.config["key_id"],
                key_version_id=Oci.config["key_version_id"]))
        logging.info(
            f"Encrypted string value - {fn.json_parse(encrypt_response.data)}")

    def decrypt(plaintext):
        """ KMS decrypt """
        logging.info("Decrypting string with KMS")
        decrypt_response = Oci.oci_key_client.decrypt(
            decrypt_data_details=oci.key_management.models.DecryptDataDetails(
                ciphertext=plaintext,
                key_id=Oci.config["key_id"],
                key_version_id=Oci.config["key_version_id"]))
        data = fn.base64_decode(decrypt_response)
        logging.info(f"Decrypted string - {data}")

    def retrieve_oci_vault_key_id():
        key_management_client = oci.key_management.KmsManagementClient(Oci.config, Oci.service_endpoint_mgmt)
        keys = key_management_client.list_keys(Oci.config["tenancy"])
        keys_json = keys.data[0]
        print(f"this is keys - {fn.json_parse(keys_json, test='id')}")

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