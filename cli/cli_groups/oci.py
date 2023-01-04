import click


@click.group()
@click.pass_context
def oci(ctx):
    """ OCI commands """
    ctx.ensure_object(dict)


@oci.command()
@click.option('-s', '--string', help='plaintext string to encrypt', required=True)
@click.pass_context
def encrypt(ctx, string):
    """ Encrypt plaintext string with OCI KMS """
    from cli.oci_client.oci_cli import Oci
    Oci.encrypt(plaintext=string)


@oci.command()
@click.option('-s', '--string', help='plaintext string to encrypt', required=True)
@click.pass_context
def decrypt(ctx, string):
    """ Decrypt KMS encrypted string """
    from cli.oci_client.oci_cli import Oci
    Oci.decrypt(plaintext=string)

@oci.command()
@click.pass_context
def list_vaults(ctx):
    """ List KMS vaults """
    from cli.oci_client.oci_cli import Oci
    Oci.list_kms_vaults()
