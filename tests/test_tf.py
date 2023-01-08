import unittest
from click.testing import CliRunner
from cli.cli_groups import tf

class TestTerraform(unittest.TestCase):

    def test_tf_init(self):
        """ Test the Terraform init function """
        runner = CliRunner()
        result = runner.invoke(
            tf.init, ['--path', '.'])
        assert result.exit_code == 0

    def test_tf_plan(self):
        """ Test the Terraform plan function """
        runner = CliRunner()
        result = runner.invoke(tf.plan, ['--path', '.'])
        assert result.exit_code == 0


    def test_tf_apply(self):
        """ Test the Terraform apply function """
        runner = CliRunner()
        result = runner.invoke(tf.apply, ['--path', '.'])
        assert result.exit_code == 0


    def test_tf_output(self):
        """ Test the Terraform output function """
        runner = CliRunner()
        result = runner.invoke(tf.output, ['--path', '.'])
        assert result.exit_code == 0


    def test_tf_destroy(self):
        """ Test the Terraform destroy function """
        runner = CliRunner()
        result = runner.invoke(tf.destroy, ['--path', '.'])
        assert result.exit_code == 0

if __name__ == '__main__':
    unittest.main()
