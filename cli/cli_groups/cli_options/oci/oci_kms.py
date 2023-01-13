import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def kms(ctx):
    """ OCI commands """
    ctx.ensure_object(dict)


@kms.command(help_priority=1)
@click.option('-s',
              '--string',
              help='plaintext string to encrypt',
              required=True)
@click.pass_context
def decrypt(ctx, string):
    """ Decrypt KMS encrypted string """
    from cli.oci_client.oci_cli import Oci
    Oci.decrypt(plaintext=string)


@kms.command(help_priority=2)
@click.option('-s',
              '--string',
              help='plaintext string to encrypt',
              required=True)
@click.pass_context
def encrypt(ctx, string):
    """ Encrypt plaintext string with OCI KMS """
    from cli.oci_client.oci_cli import Oci
    Oci.encrypt(plaintext=string)