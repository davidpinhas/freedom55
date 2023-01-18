import click
import logging
from utils.fd55_config import Config


@click.group()
@click.pass_context
def ai(ctx):
    """ Configure OpenAI """
    ctx.ensure_object(dict)


@ai.command()
@click.option('-c', '--api-key', help='OpenAI API key', required=False)
@click.pass_context
def set(ctx, api_key=None):
    """ Set OpenAI keys """
    config = Config()
    if api_key:
        config.create_option("AI", "api_key", api_key)
    if not any([api_key]):
        logging.warning("At least one parameter is required.")
