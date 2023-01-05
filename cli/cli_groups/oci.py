import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def oci(ctx):
    """ OCI commands """
    ctx.ensure_object(dict)


<<<<<<< HEAD
@oci.command()
@click.option('-s',
              '--string',
              help='plaintext string to encrypt',
              required=True)
@click.pass_context
def encrypt(ctx, string):
    """ Encrypt plaintext string with OCI KMS """
    from cli.oci_client.oci_cli import Oci
    Oci.encrypt(plaintext=string)


@oci.command()
@click.option('-s',
              '--string',
              help='plaintext string to encrypt',
              required=True)
=======
@oci.command(help_priority=1)
@click.option('-s', '--string', help='plaintext string to encrypt', required=True)
>>>>>>> a6bb98e (set help commands order and revised cli groups)
@click.pass_context
def decrypt(ctx, string):
    """ Decrypt KMS encrypted string """
    from cli.oci_client.oci_cli import Oci
    Oci.decrypt(plaintext=string)

<<<<<<< HEAD

@oci.command()
@click.option('--id', help="Display vaults IDs", is_flag=True)
=======
@oci.command(help_priority=2)
@click.option('-s', '--string', help='plaintext string to encrypt', required=True)
@click.pass_context
def encrypt(ctx, string):
    """ Encrypt plaintext string with OCI KMS """
    from cli.oci_client.oci_cli import Oci
    Oci.encrypt(plaintext=string)

@oci.command(help_priority=3)
@click.option('--id' ,help="Display vaults IDs" , is_flag=True)
>>>>>>> a6bb98e (set help commands order and revised cli groups)
@click.pass_context
def list_vaults(ctx, id):
    """ List KMS vaults """
    from cli.oci_client.oci_cli import Oci
    if id:
        Oci.list_kms_vaults(id=True)
    else:
        Oci.list_kms_vaults()

<<<<<<< HEAD

@oci.command()
=======
@oci.command(help_priority=4)
>>>>>>> a6bb98e (set help commands order and revised cli groups)
@click.option('-n', '--name', help='Vault name', required=True)
@click.pass_context
def create_vault(ctx, name):
    """ Create vault """
    from cli.oci_client.oci_cli import Oci
    Oci.create_vault(name=name)

<<<<<<< HEAD

@oci.command()
=======
@oci.command(help_priority=5)
>>>>>>> a6bb98e (set help commands order and revised cli groups)
@click.option('--id', help='Vault ID', required=True)
@click.option('-d',
              '--days',
              help='Number of days from today to schedule the vault deletion',
              required=False)
@click.pass_context
def delete_vault(ctx, id, days):
    """ Schedule vault deletion """
    from cli.oci_client.oci_cli import Oci
    if days:
        Oci.delete_vault(vault_id=id, days=days)
    else:
        Oci.delete_vault(vault_id=id)
