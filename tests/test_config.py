import unittest
from click.testing import CliRunner
from fd55.cli.cli_groups.integration_cli_config import cli_config_argocd, cli_config_cloudflare, cli_config_oci, cli_config_sops
unittest.TestLoader.sortTestMethodsUsing = None


class TestConfig(unittest.TestCase):

    def test1_config_set_argocd(self):
        """ Test the Config argo set function """
        runner = CliRunner()
        result = runner.invoke(
            cli_config_argocd.set, [
                '--url', 'https://argo.domain.com', '--api-token', 'Token'])
        assert result.exit_code == 0

    def test2_config_set_cloudflare(self):
        """ Test the Config cloudflare set function """
        runner = CliRunner()
        result = runner.invoke(
            cli_config_cloudflare.set, [
                '--email', 'test@gmail.com', '--api-key', 'Key', '--domain-name', 'domain.com'])
        assert result.exit_code == 0

    def test3_config_set_oci(self):
        """ Test the Config oci set function """
        runner = CliRunner()
        result = runner.invoke(cli_config_oci.set,
                               ['--user',
                                'test1',
                                '--fingerprint',
                                'test2',
                                '--tenancy',
                                'test3',
                                '--region',
                                'test4',
                                '--key-file',
                                'test5'])
        assert result.exit_code == 0

    def test4_config_set_sops(self):
        """ Test the Config sops set function """
        runner = CliRunner()
        result = runner.invoke(
            cli_config_sops.set, ['--key-file', 'key.txt'])
        assert result.exit_code == 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    unittest.TestLoader.sort_test_methods_by_name(
        suite, sort_key=lambda x: x.lower())
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
