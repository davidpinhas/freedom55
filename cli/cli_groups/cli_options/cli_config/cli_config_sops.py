import click
import logging
from utils.fd55_config import Config


@click.group()
@click.pass_context
def sops(ctx):
    """ Configure SOPS """
    ctx.ensure_object(dict)


@sops.command()
@click.option('-k', '--key_file', help='SOPS key file', required=False)
@click.pass_context
def set(ctx, key_file=None):
    """ Set SOPS keys """
    config = Config()
    if key_file:
        config.create_option("SOPS", "key_file", key_file)
    if not any([key_file]):
        logging.warning("At least one parameter is required.")
