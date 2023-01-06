import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def cf(ctx):
    """ Cloudflare commands """
    ctx.ensure_object(dict)


@cf.command(help_priority=1)
@click.pass_context
def update_dns(ctx):
    """ Update DNS record """
    pass
