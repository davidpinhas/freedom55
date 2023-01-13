import click
from cli.cli_groups.cli_options.cli_config import cli_config_argocd
from cli.cli_groups.cli_options.cli_config import cli_config_cloudflare
from cli.cli_groups.cli_options.cli_config import cli_config_oci
from cli.cli_groups.cli_options.cli_config import cli_config_sops
from utils.cli_help_order import CliHelpOrder



@click.group(cls=CliHelpOrder)
@click.pass_context
def config(ctx):
    """ Configure Freedom 55 """
    ctx.ensure_object(dict)


@config.command(help_priority=0)
@click.pass_context
def start(ctx):
    """ Configure CLI """
    from utils.fd55_config import Config
    config = Config()
    config.run_config_validation()


config.add_command(cli_config_argocd.argo)
config.add_command(cli_config_cloudflare.cf)
config.add_command(cli_config_oci.oci)
config.add_command(cli_config_sops.sops)