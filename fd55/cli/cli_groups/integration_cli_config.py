import click
from fd55.cli.cli_groups.cli_options.cli_config import cli_config_argocd
from fd55.cli.cli_groups.cli_options.cli_config import cli_config_cloudflare
from fd55.cli.cli_groups.cli_options.cli_config import cli_config_oci
from fd55.cli.cli_groups.cli_options.cli_config import cli_config_sops
from fd55.cli.cli_groups.cli_options.cli_config import cli_config_ai
from fd55.cli.cli_groups.cli_options.cli_config import cli_config_nexus
from fd55.utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def config(ctx):
    """ Configure Freedom 55 """
    ctx.ensure_object(dict)


@config.command(help_priority=0)
@click.pass_context
def start(ctx):
    """ Configure CLI """
    from fd55.utils.fd55_config import Config
    config = Config()
    config.run_config_validation()


config.add_command(cli_config_argocd.argo)
config.add_command(cli_config_cloudflare.cf)
config.add_command(cli_config_oci.oci)
config.add_command(cli_config_sops.sops)
config.add_command(cli_config_ai.ai)
config.add_command(cli_config_nexus.nexus)