import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def server(ctx):
    """ application commands """
    ctx.ensure_object(dict)


@server.command(help_priority=1)
@click.pass_context
def export(ctx):
    """ Export ArgoCD server settings """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.export_argocd_settings()