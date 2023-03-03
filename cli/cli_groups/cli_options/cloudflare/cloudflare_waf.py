import click
from utils.cli_help_order import CliHelpOrder
from cli.cloudflare_client.cloudflare_cli import Cloudflare
from utils.fd55_config import Config
from utils.functions import Functions as fn


@click.group(cls=CliHelpOrder)
@click.pass_context
def waf(ctx):
    """ Cloudflare WAF commands """
    ctx.ensure_object(dict)
    config = Config()
    if not config.get(section="CLOUDFLARE", option="global_api_key"):
        user_input = fn.modify_config_approval(
            "No global API key configure, would you like to configure it now? Y/n: ")
        if user_input:
            input(f'Enter the value for global_api_key: ')


@waf.command(help_priority=1)
@click.pass_context
def list(ctx):
    """ List firewall rules """
    Cloudflare().list_waf_rules()


@waf.command(help_priority=2)
@click.pass_context
def create(
        ctx,
        action,
        expression,
        id=None,
        paused=None,
        description=None,
        priority=None):
    """ Create firewall rule """
    Cloudflare().create_waf_rule(
        action=action,
        expression=expression,
        id=id,
        paused=paused,
        description=description,
        priority=priority)
