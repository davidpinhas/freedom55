import unittest
from click.testing import CliRunner
from cli.cli_groups import integration_sops
unittest.TestLoader.sortTestMethodsUsing = None


class TestSops(unittest.TestCase):

    def test1_sops_encrypt(self):
        """ Test the SOPS encrypt function """
        runner = CliRunner()
        result = runner.invoke(integration_sops.encrypt,
                               ['--input_file',
                                'test-values.yaml',
                                '--output_file',
                                'enc-values.yaml',
                                '--key_file',
                                'key.txt'])
        assert result.exit_code == 0

    def test2_sops_decrypt(self):
        """ Test the SOPS decrypt function """
        runner = CliRunner()
        result = runner.invoke(integration_sops.decrypt,
                               ['--input_file',
                                'enc-values.yaml',
                                '--output_file',
                                'test-values.yaml',
                                '--key_file',
                                'key.txt'])
        assert result.exit_code == 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSops)
    unittest.TestLoader.sort_test_methods_by_name(
        suite, sort_key=lambda x: x.lower())
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
