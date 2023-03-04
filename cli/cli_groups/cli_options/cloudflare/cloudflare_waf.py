import click
from utils.cli_help_order import CliHelpOrder
from cli.cloudflare_client.cloudflare_cli import Cloudflare
from utils.fd55_config import Config
from utils.functions import Functions as fn
import logging


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
@click.option('-n',
              '--name',
              help="name of the firewall rule")
@click.option('-a',
              '--action',
              help="select rule action, valid values: (allow,block). 'block' used by default",
              default='block')
@click.option('-e',
              '--expression',
              help='set rule expression',
              required=True)
@click.option('-p',
              '--paused',
              help='set if the rule is pasued, valid values: (true,false)',
              is_flag=True,
              default=False)
@click.option('-d',
              '--description',
              help='rule description',
              required=False)
@click.pass_context
def create(
        ctx,
        expression,
        paused=False,
        action=None,
        name=None,
        description=None):
    """ Create firewall rule """
    Cloudflare().create_waf_rule(
        name=name,
        action=action,
        expression=expression,
        paused=paused,
        description=description)


@waf.command(help_priority=3)
@click.option('--id', help="rule id to update")
@click.option('-n',
              '--name',
              help="firewall rule name")
@click.option('-a',
              '--action',
              help="select rule action, valid values: (allow,block). 'block' used by default",
              default='block')
@click.option('-e',
              '--expression',
              help='set rule expression',
              required=True)
@click.option('-p',
              '--paused',
              help='set if the rule is pasued, valid values: (true,false)',
              is_flag=True,
              default=False)
@click.option('-d',
              '--description',
              help='rule filter description',
              required=False)
@click.pass_context
def update(ctx, 
        id, 
        expression,
        paused=False,
        action=None,
        name=None,
        description=None):
    """ Update firewall rule """
    Cloudflare().update_waf_rule(
        id=id, 
        name=name,
        action=action,
        expression=expression,
        paused=paused,
        description=description)


@waf.command(help_priority=4)
@click.pass_context
@click.option('-n', '--name', help='name of the rule', required=False)
@click.option('--id', help='rule id', required=False)
def delete(ctx, name=None, id=None):
    """ Delete firewall rule """
    if name or id:
        Cloudflare().delete_waf_rule(name=name, id=id)
    else:
        logging.error("Requires name or id flag")


@waf.command(help_priority=5)
@click.pass_context
def list_filters(ctx):
    """ List firewall rules filters """
    Cloudflare().list_waf_rule_filters()


@waf.command(help_priority=6)
@click.pass_context
@click.option('--id', help='rule id', required=True)
def delete_filter(ctx, id=None):
    """ Delete firewall rule filter """
    Cloudflare().delete_waf_rule_filter(id=id)
