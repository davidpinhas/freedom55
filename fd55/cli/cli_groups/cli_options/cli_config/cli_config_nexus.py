import click
import logging
from fd55.utils.fd55_config import Config


@click.group()
@click.pass_context
def nexus(ctx):
    """ Configure Nexus Repository Manager """
    ctx.ensure_object(dict)


@nexus.command()
@click.option('--url', help='Nexus Repository Manager URL', required=False)
@click.option('-u', '--user', help='Admin username', required=False)
@click.option('-p', '--password', help='Admin password', required=False)
@click.pass_context
def set(ctx, url=None, user=None, password=None):
    """ Set Nexus keys """
    config = Config()
    if url:
        config.create_option("NEXUS", "url", url)
    if user:
        config.create_option("NEXUS", "user", user)
    if password:
        config.create_option("NEXUS", "password", password)
    if not any([url, user, password]):
        logging.warning("At least one parameter is required.")
