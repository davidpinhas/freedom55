import unittest
from click.testing import CliRunner
from cli.cli_groups.integration_oci import oci_kms, oci_vault
from cli.oci_client.oci_cli import Oci


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

    def test_set_vault(self):
        """ Test the set_vault function """
        runner = CliRunner()
        result = runner.invoke(oci_vault.set, ['--name', 'test-vault'])
        assert result.exit_code == 0

    def test_create_vault(self):
        """ Test the create_vault function """
        runner = CliRunner()
        result = runner.invoke(oci_vault.create, ['--name', 'test'])
        assert result.exit_code == 0

    def test_delete_vault(self):
        """ Test the delete_vault function """
        runner = CliRunner()
        result = runner.invoke(
            oci_vault.delete, [
                '--id', 'ocid1.vault.oc1', '--days', '7'])
        assert result.exit_code == 0


if __name__ == '__main__':
    unittest.main()
