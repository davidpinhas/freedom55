import click
from cli.tf_client.tf_cli import TerraformCli


@click.group()
@click.pass_context
def tf(ctx):
    """ Terraform commands """
    ctx.ensure_object(dict)


@tf.command()
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def init(ctx, path):
    """ Init your working directory """
    TerraformCli.tf_init(path)


@tf.command()
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def plan(ctx, path):
    """ Run Terraform plan on the selected path """
    TerraformCli.tf_plan(path)


@tf.command()
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def apply(ctx, path):
    """ Apply the changes """
    TerraformCli.tf_apply(path)


@tf.command()
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def output(ctx, path):
    """ Get output of Terraform project """
    TerraformCli.tf_output(path)


@tf.command()
@click.option('-p', '--path', help='path of Terraform project', required=True)
@click.pass_context
def destroy(ctx, path):
    """ Destroy infrastructure """
    TerraformCli.tf_destroy(path)