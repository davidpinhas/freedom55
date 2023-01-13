import click


@click.group()
@click.pass_context
def config(ctx):
    """ Configure Freedom 55 """
    ctx.ensure_object(dict)


@config.command()
@click.pass_context
def start(ctx):
    """ Configure CLI """
    from utils.fd55_config import Config
    config = Config()
    config.run_config_validation()
