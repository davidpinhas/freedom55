import click
from utils.cli_help_order import CliHelpOrder
from cli.cloudflare_client.cloudflare_cli import Cloudflare


@click.group(cls=CliHelpOrder)
@click.pass_context
def waf(ctx):
    """ Cloudflare WAF commands """
    ctx.ensure_object(dict)


@waf.command(help_priority=1)
@click.pass_context
def list(ctx):
    """ List firewall rules """
    Cloudflare().list_waf_rules()
