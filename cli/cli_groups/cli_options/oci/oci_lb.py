import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def lb(ctx):
    """ OCI load balancer commands """
    ctx.ensure_object(dict)


@lb.command(help_priority=1)
@click.option('--id', help="Display vaults IDs", is_flag=True)
@click.pass_context
def list(ctx, id):
    """ List load balancers """
    from cli.oci_client.oci_cli import Oci
    if id:
        Oci.list_lb(id=True)
    else:
        Oci.list_lb()
