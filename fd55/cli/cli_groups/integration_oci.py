import click
from fd55.cli.cli_groups.cli_options.oci import oci_kms, oci_vault, oci_network


@click.group()
@click.pass_context
def oci(ctx):
    """ OCI Commands """
    ctx.ensure_object(dict)


oci.add_command(oci_kms.kms)
oci.add_command(oci_vault.vault)
oci.add_command(oci_network.network)
