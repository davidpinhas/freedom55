import unittest
from click.testing import CliRunner
from cli.cli_groups import argocd
unittest.TestLoader.sortTestMethodsUsing = None


class TestArgo(unittest.TestCase):

    def test1_argo_list_apps(self):
        """ Test the Argo list_apps function """
        runner = CliRunner()
        result = runner.invoke(
            argocd.get_apps)
        assert result.exit_code == 0

    def test2_argo_create_app(self):
        """ Test the Argo create_app function """
        runner = CliRunner()
        result = runner.invoke(
            argocd.create_app, [
                '--file', 'tmp_argo_app.json'])
        assert result.exit_code == 0

    def test3_argo_update_app(self):
        """ Test the Argo update_app function """
        runner = CliRunner()
        result = runner.invoke(
            argocd.update_app, [
                '--file', 'tmp_argo_app.json'])
        assert result.exit_code == 0

    def test4_argo_delete_app(self):
        """ Test the Argo delete_app function """
        runner = CliRunner()
        result = runner.invoke(
            argocd.delete_app, [
                '--name', 'freedom55_argo_test_app'])
        assert result.exit_code == 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArgo)
    unittest.TestLoader.sort_test_methods_by_name(
        suite, sort_key=lambda x: x.lower())
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()