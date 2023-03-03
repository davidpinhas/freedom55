import unittest
from click.testing import CliRunner
from cli.cli_groups.integration_cloudflare import cloudflare_dns
from cli.cli_groups.integration_cloudflare import cloudflare_waf
from utils.fd55_config import Config
unittest.TestLoader.sortTestMethodsUsing = None
config = Config()


class TestCloudflare(unittest.TestCase):
    def test1_list_dns(self):
        """ Test the list_dns function """
        runner = CliRunner()
        result = runner.invoke(cloudflare_dns.list, ['--id'])
        assert result.exit_code == 0

    def test2_create_dns(self):
        """ Test the create_dns function """
        runner = CliRunner()
        result = runner.invoke(cloudflare_dns.create,
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
        result = runner.invoke(cloudflare_dns.update,
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
            cloudflare_dns.delete, [
                '--name', f'freedom55.test.{config.get("CLOUDFLARE", "domain_name")}'])
        assert result.exit_code == 0

    def test5_list_waf_rules(self):
        """ Test the list_waf_rules function """
        runner = CliRunner()
        result = runner.invoke(cloudflare_waf.list)
        assert result.exit_code == 0

    def test6_list_waf_rules_filters(self):
        """ Test the list_waf_rules_filters function """
        runner = CliRunner()
        result = runner.invoke(cloudflare_waf.list_filters)
        assert result.exit_code == 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCloudflare)
    unittest.TestLoader.sort_test_methods_by_name(
        suite, sort_key=lambda x: x.lower())
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
