import click
from fd55.utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def tf(ctx):
    """ Terraform commands """
    ctx.ensure_object(dict)


@tf.command(help_priority=1)
@click.option('-p', '--path', help='Path of Terraform project', required=True)
@click.pass_context
def init(ctx, path):
    """ Init your working directory """
    from fd55.cli.tf_client.tf_cli import TerraformCli
    tf = TerraformCli(working_dir=path)
    tf.tf_init()


@tf.command(help_priority=2)
@click.option('-p', '--path', help='Path of Terraform project', required=True)
@click.option('-f', '--file', help='path to Terraform plan file', required=True)
@click.pass_context
def plan(ctx, path, file):
    """ Run Terraform plan on the selected path """
    from fd55.cli.tf_client.tf_cli import TerraformCli
    tf = TerraformCli(working_dir=path)
    tf.tf_plan(outfile=file)


@tf.command(help_priority=3)
@click.option('-p', '--path', help='Path of Terraform project', required=True)
@click.option('-f', '--planfile', help='Path to Terraform plan file', required=True)
@click.pass_context
def apply(ctx, path, planfile):
    """ Apply the changes """
    from fd55.cli.tf_client.tf_cli import TerraformCli
    tf = TerraformCli(working_dir=path)
    tf.tf_apply(planfile=planfile)


@tf.command(help_priority=4)
@click.option('-p', '--path', help='Path of Terraform project', required=True)
@click.pass_context
def output(ctx, path):
    """ Get output of Terraform project """
    from fd55.cli.tf_client.tf_cli import TerraformCli
    tf = TerraformCli(working_dir=path)
    tf.tf_output()


@tf.command(help_priority=5)
@click.option('-p', '--path', help='Path of Terraform project', required=True)
@click.pass_context
def destroy(ctx, path):
    """ Destroy infrastructure """
    from fd55.cli.tf_client.tf_cli import TerraformCli
    tf = TerraformCli(working_dir=path)
    tf.tf_destroy()
