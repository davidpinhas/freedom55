import unittest
from click.testing import CliRunner
from fd55.cli.cli_groups.integration_argocd import argocd_app, argocd_repo
unittest.TestLoader.sortTestMethodsUsing = None


class TestArgo(unittest.TestCase):

    def test1_argo_list_apps(self):
        """ Test the Argo list_apps function """
        runner = CliRunner()
        result = runner.invoke(
            argocd_app.list)
        assert result.exit_code == 0

    def test2_argo_create_app(self):
        """ Test the Argo create_app function """
        runner = CliRunner()
        result = runner.invoke(
            argocd_app.create, [
                '--file', 'tmp_argo_app.json'])
        assert result.exit_code == 0

    def test3_argo_update_app(self):
        """ Test the Argo update_app function """
        runner = CliRunner()
        result = runner.invoke(
            argocd_app.update, [
                '--file', 'tmp_argo_app.json'])
        assert result.exit_code == 0

    def test4_argo_delete_app(self):
        """ Test the Argo delete_app function """
        runner = CliRunner()
        result = runner.invoke(
            argocd_app.delete, [
                '--name', 'freedom55-argo-test-app'])
        assert result.exit_code == 0

    def test5_argo_list_repos(self):
        """ Test the Argo list_repos function """
        runner = CliRunner()
        result = runner.invoke(argocd_repo.list)
        assert result.exit_code == 0

    def test6_argo_add_repo(self):
        """ Test the Argo add_repo function """
        runner = CliRunner()
        result = runner.invoke(argocd_repo.add, [
            '--repo-url', 'https://github.com/davidpinhas/mc-server.git'])
        assert result.exit_code == 0

    def test7_argo_update_repo(self):
        """ Test the Argo update_repo function """
        runner = CliRunner()
        result = runner.invoke(argocd_repo.update, [
            '--repo-url', 'https://github.com/davidpinhas/mc-server.git'])
        assert result.exit_code == 0

    def test8_argo_delete_repo(self):
        """ Test the Argo delete_repo function """
        runner = CliRunner()
        result = runner.invoke(
            argocd_repo.delete, [
                '--repo-url', 'https://github.com/davidpinhas/mc-server.git'])
        assert result.exit_code == 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArgo)
    unittest.TestLoader.sort_test_methods_by_name(
        suite, sort_key=lambda x: x.lower())
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
