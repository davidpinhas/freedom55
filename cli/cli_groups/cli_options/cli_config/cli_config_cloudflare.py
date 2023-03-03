import click
import logging
from utils.fd55_config import Config


@click.group()
@click.pass_context
def cf(ctx=None):
    """ Configure Cloudflare """
    ctx.ensure_object(dict)


@cf.command()
@click.option('-u', '--email', help='User email', required=False)
@click.option('-p', '--api-key', help='Cloudflare API key', required=False)
@click.option('-g', '--global-api-key', help='Cloudflare Global API key', required=False)
@click.option('-d',
              '--domain-name',
              help='Cloudflare domain name',
              required=False)
@click.pass_context
def set(ctx, email=None, api_key=None, global_api_key=None, domain_name=None):
    """ Set Cloudflare keys """
    config = Config()
    if email:
        config.create_option("CLOUDFLARE", "email", email)
    if api_key:
        config.create_option("CLOUDFLARE", "api_key", api_key)
    if global_api_key:
        config.create_option("CLOUDFLARE", "global_api_key", global_api_key)
    if domain_name:
        config.create_option("CLOUDFLARE", "domain_name", domain_name)
    if not any([email, api_key, global_api_key, domain_name]):
        logging.warning("At least one parameter is required.")
