import click

@click.group()
@click.pass_context
def argo(ctx):
    """ ArgoCD commands """
    ctx.ensure_object(dict)


@argo.command()
@click.pass_context
def get_apps(ctx):
    """ Get ArgoCD applications """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(api_endpoint=f"{config.get('ARGOCD', 'url')}", api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.get_applications()

@argo.command()
@click.option('-f', '--file', help='application yaml file', required=True)
@click.pass_context
def create_app(ctx, file):
    """ Create an ArgoCD application """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(api_endpoint=f"{config.get('ARGOCD', 'url')}", api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.create_application(json_file=file)

@argo.command()
@click.option('-f', '--file', help='application yaml file', required=True)
@click.pass_context
def update_app(ctx, file):
    """ Update an ArgoCD application """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(api_endpoint=f"{config.get('ARGOCD', 'url')}", api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.update_application(json_file=file)

@argo.command()
@click.option('-n', '--name', help='application name', required=True)
@click.pass_context
def delete_app(ctx, name):
    """ Delete an ArgoCD application """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(api_endpoint=f"{config.get('ARGOCD', 'url')}", api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.delete_application(application_name=name)
