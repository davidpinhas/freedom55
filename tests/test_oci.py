import unittest
from click.testing import CliRunner
from cli.cli_groups import oci
from cli.oci_client.oci_cli import Oci


class TestOci(unittest.TestCase):
    kms_encrypted_value = Oci.encrypt(plaintext='test')

    def test_decrypt(self):
        # Test the decrypt function
        runner = CliRunner()
        result = runner.invoke(
            oci.decrypt, [
                '-s', f'{TestOci.kms_encrypted_value}'])
        assert result.exit_code == 0

    def test_encrypt(self):
        # Test the encrypt function
        runner = CliRunner()
        result = runner.invoke(oci.encrypt, ['-s', 'test'])
        assert result.exit_code == 0

    def test_list_vaults(self):
        # Test the list_vaults function
        runner = CliRunner()
        result = runner.invoke(oci.list_vaults, ['--id'])
        assert result.exit_code == 0

    def test_create_vault(self):
        # Test the create_vault function
        runner = CliRunner()
        result = runner.invoke(oci.create_vault, ['-n', 'test'])
        assert result.exit_code == 0

    def test_delete_vault(self):
        # Test the delete_vault function
        runner = CliRunner()
        result = runner.invoke(
            oci.delete_vault, [
                '--id', 'ocid1.vault.oc1', '--days', '7'])
        assert result.exit_code == 0


if __name__ == '__main__':
    unittest.main()
