import click
from cli.cli_groups.cli_options.oci import oci_kms, oci_vault


@click.group()
@click.pass_context
def oci(ctx):
    """ OCI Commands """
    ctx.ensure_object(dict)


oci.add_command(oci_kms.kms)
oci.add_command(oci_vault.vault)
