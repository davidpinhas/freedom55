import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def tf(ctx):
    """ Terraform commands """
    ctx.ensure_object(dict)


@tf.command(help_priority=1)
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def init(ctx, path):
    """ Init your working directory """
    from cli.tf_client.tf_cli import TerraformCli
    TerraformCli.tf_init(path)


@tf.command(help_priority=2)
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def plan(ctx, path):
    """ Run Terraform plan on the selected path """
    from cli.tf_client.tf_cli import TerraformCli
    TerraformCli.tf_plan(path)


@tf.command(help_priority=3)
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def apply(ctx, path):
    """ Apply the changes """
    from cli.tf_client.tf_cli import TerraformCli
    TerraformCli.tf_apply(path)


@tf.command(help_priority=4)
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def output(ctx, path):
    """ Get output of Terraform project """
    from cli.tf_client.tf_cli import TerraformCli
    TerraformCli.tf_output(path)


@tf.command(help_priority=5)
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def destroy(ctx, path):
    """ Destroy infrastructure """
    from cli.tf_client.tf_cli import TerraformCli
    TerraformCli.tf_destroy(path)
