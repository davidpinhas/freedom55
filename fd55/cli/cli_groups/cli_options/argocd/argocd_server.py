import click
from fd55.utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def server(ctx):
    """ application commands """
    ctx.ensure_object(dict)


@server.command(help_priority=1)
@click.pass_context
def export(ctx):
    """ Export ArgoCD server settings """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.export_argocd_settings()


@server.command(name='import', help_priority=2)
@click.option('-f', '--file', help="ArgoCD backup file", required=True)
@click.pass_context
def import_command(ctx, file):
    """ Import ArgoCD server settings """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.import_argocd_settings(file=file)
