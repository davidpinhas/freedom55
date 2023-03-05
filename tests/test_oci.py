import unittest
from click.testing import CliRunner
from fd55.cli.cli_groups.integration_oci import oci_kms, oci_vault
from fd55.cli.oci_client.oci_cli import Oci


class TestOci(unittest.TestCase):
    kms_encrypted_value = Oci.encrypt(plaintext='test')

    def test_decrypt(self):
        """ Test the decrypt function """
        runner = CliRunner()
        result = runner.invoke(
            oci_kms.decrypt, [
                '--string', f'{TestOci.kms_encrypted_value}'])
        assert result.exit_code == 0

    def test_encrypt(self):
        """ Test the encrypt function """
        runner = CliRunner()
        result = runner.invoke(oci_kms.encrypt, ['--string', 'test'])
        assert result.exit_code == 0

    def test_list_vaults(self):
        """ Test the list_vaults function """
        runner = CliRunner()
        result = runner.invoke(oci_vault.list, ['--id'])
        assert result.exit_code == 0


if __name__ == '__main__':
    unittest.main()
