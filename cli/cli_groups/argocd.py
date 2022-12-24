import click
from cli.argocd_client.argocd_cli import ArgoCD
from utils.fd55_config import Config

config = Config()
@click.group()
@click.pass_context
def argo(ctx):
    """ ArgoCD commands """
    ctx.ensure_object(dict)


@argo.command()
@click.pass_context
def get_apps(ctx):
    """ Get ArgoCD applications """
    argo = ArgoCD(api_endpoint=f"{config.get('ARGOCD', 'url')}", api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.get_applications()

@argo.command()
@click.option('--app-name', help='Set the application name', required=True)
@click.option('--repo', help='Set the repository URL', required=True)
@click.pass_context
def create_app(ctx, application_name, repository_url):
    """ Create an ArgoCD application """
    ArgoCD.create_application(application_name, repository_url)
