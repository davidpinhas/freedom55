import click
from fd55.utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def vault(ctx):
    """ OCI KMS vault commands """
    ctx.ensure_object(dict)


@vault.command(help_priority=1)
@click.option('--id', help="Display vaults IDs", is_flag=True)
@click.pass_context
def list(ctx, id):
    """ List KMS vaults """
    from fd55.cli.oci_client.oci_cli import Oci
    if id:
        Oci.list_kms_vaults(id=True)
    else:
        Oci.list_kms_vaults()


@vault.command(help_priority=2)
@click.option('-n', '--name', help="Vault name", required=False)
@click.pass_context
def set(ctx, name):
    """ Set default KMS vault """
    from fd55.cli.oci_client.oci_cli import OciValidator
    OciValidator.setup_kms_vault(vault_name=name)


@vault.command(help_priority=3)
@click.option('-n', '--name', help='Vault name', required=True)
@click.pass_context
def create(ctx, name):
    """ Create vault """
    from fd55.cli.oci_client.oci_cli import Oci
    Oci.create_vault(name=name)


@vault.command(help_priority=4)
@click.option('--id', help='Vault ID', required=True)
@click.option('-d',
              '--days',
              help='Number of days from today to schedule the vault deletion',
              required=False)
@click.pass_context
def delete(ctx, id, days):
    """ Schedule vault deletion """
    from fd55.cli.oci_client.oci_cli import Oci
    if days:
        Oci.delete_vault(vault_id=id, days=days)
    else:
        Oci.delete_vault(vault_id=id)
