import unittest
from click.testing import CliRunner
from cli.cli_groups import cloudflare
from utils.fd55_config import Config
unittest.TestLoader.sortTestMethodsUsing = None
config = Config()


class TestCloudflare(unittest.TestCase):
    def test1_list_dns(self):
        """ Test the list_dns function """
        runner = CliRunner()
        result = runner.invoke(cloudflare.list_dns, ['--id'])
        assert result.exit_code == 0

    def test2_create_dns(self):
        """ Test the create_dns function """
        runner = CliRunner()
        result = runner.invoke(cloudflare.create_dns,
                               ['--name',
                                f'freedom55.test.{config.get("CLOUDFLARE", "domain_name")}',
                                '--content',
                                '@',
                                '--type',
                                'CNAME',
                                '--proxied',
                                '--comment',
                                'test'])
        assert result.exit_code == 0

    def test3_update_dns(self):
        """ Test the update_dns function """
        runner = CliRunner()
        result = runner.invoke(cloudflare.update_dns,
                               ['--name',
                                f'freedom55.test.{config.get("CLOUDFLARE", "domain_name")}',
                                '--content',
                                '127.0.0.1',
                                '--type',
                                'A'])
        assert result.exit_code == 0

    def test4_delete_dns(self):
        """ Test the delete_dns function """
        runner = CliRunner()
        result = runner.invoke(
            cloudflare.delete_dns, [
                '--name', f'freedom55.test.{config.get("CLOUDFLARE", "domain_name")}'])
        assert result.exit_code == 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCloudflare)
    unittest.TestLoader.sort_test_methods_by_name(
        suite, sort_key=lambda x: x.lower())
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
