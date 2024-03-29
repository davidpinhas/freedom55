import click
from fd55.utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def server(ctx):
    """ ArgoCD server commands """
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
@click.pass_context
def import_command(ctx):
    """ Import ArgoCD server settings """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.import_argocd_settings()


@server.command(help_priority=3)
@click.option('-u', '--user', help="ArgoCD admin user", required=True)
@click.option('-p', '--password', help="ArgoCD admin password", required=True)
@click.pass_context
def create_jwt(ctx, user, password):
    """ Create a new JWT for authentication """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}")
    argo.create_jwt(username=user, password=password)
