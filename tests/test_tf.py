import unittest
from click.testing import CliRunner
from fd55.cli.cli_groups import integration_tf


class TestTerraform(unittest.TestCase):

    def test1_tf_init(self):
        """ Test the Terraform init function """
        runner = CliRunner()
        result = runner.invoke(
            integration_tf.init, ['--path', '.'])
        assert result.exit_code == 0

    def test2_tf_plan(self):
        """ Test the Terraform plan function """
        runner = CliRunner()
        result = runner.invoke(
            integration_tf.plan, [
                '--path', '.', '--file', 'tfplan'])
        assert result.exit_code == 0

    def test3_tf_apply(self):
        """ Test the Terraform apply function """
        runner = CliRunner()
        result = runner.invoke(
            integration_tf.apply, [
                '--path', '.', '--planfile', 'tfplan'])
        assert result.exit_code == 0

    def test4_tf_output(self):
        """ Test the Terraform output function """
        runner = CliRunner()
        result = runner.invoke(integration_tf.output, ['--path', '.'])
        assert result.exit_code == 0

    def test5_tf_destroy(self):
        """ Test the Terraform destroy function """
        runner = CliRunner()
        result = runner.invoke(integration_tf.destroy, ['--path', '.'])
        assert result.exit_code == 0


if __name__ == '__main__':
    unittest.main()
