import click
from cli.argocd_client.argocd_cli import ArgoCD


@click.group()
@click.pass_context
def argo(ctx):
    """ ArgoCD commands """
    ctx.ensure_object(dict)


@argo.command()
@click.pass_context
def get_apps(ctx):
    """ Get ArgoCD applications """
    argo_url = ArgoCD(api_endpoint="https://example.com", api_token=None)
    argo_url.get_applications()

@argo.command()
@click.option('--app-name', help='Set the application name', required=True)
@click.option('--repo', help='Set the repository URL', required=True)
@click.pass_context
def create_app(ctx, application_name, repository_url):
    """ Create an ArgoCD application """
    ArgoCD.create_application(application_name, repository_url)
