import click
from utils.fd55_config import Config


@click.group()
@click.pass_context
def config(ctx):
    """ Configure Freedom 55 """
    ctx.ensure_object(dict)


@config.command()
@click.pass_context
def config(ctx):
    """ Configure CLI """
    config = Config()
    config.run_config_validation()
