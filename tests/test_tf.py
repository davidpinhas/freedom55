import unittest
from click.testing import CliRunner
from fd55.cli.cli_groups import integration_tf


class TestTerraform(unittest.TestCase):

    def test_tf_init(self):
        """ Test the Terraform init function """
        runner = CliRunner()
        result = runner.invoke(
            integration_tf.init, ['--path', '.'])
        assert result.exit_code == 0

    def test_tf_plan(self):
        """ Test the Terraform plan function """
        runner = CliRunner()
        result = runner.invoke(integration_tf.plan, ['--path', '.'])
        assert result.exit_code == 0

    def test_tf_apply(self):
        """ Test the Terraform apply function """
        runner = CliRunner()
        result = runner.invoke(integration_tf.apply, ['--path', '.'])
        assert result.exit_code == 0

    def test_tf_output(self):
        """ Test the Terraform output function """
        runner = CliRunner()
        result = runner.invoke(integration_tf.output, ['--path', '.'])
        assert result.exit_code == 0

    def test_tf_destroy(self):
        """ Test the Terraform destroy function """
        runner = CliRunner()
        result = runner.invoke(integration_tf.destroy, ['--path', '.'])
        assert result.exit_code == 0


if __name__ == '__main__':
    unittest.main()
