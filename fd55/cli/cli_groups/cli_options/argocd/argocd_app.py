import click
from fd55.utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def app(ctx):
    """ application commands """
    ctx.ensure_object(dict)


@app.command(help_priority=1)
@click.pass_context
def list(ctx):
    """ Get ArgoCD applications """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.get_applications()


@app.command(help_priority=2)
@click.option('-f', '--file', help='application yaml file', required=True)
@click.pass_context
def create(ctx, file):
    """ Create an ArgoCD application """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.create_application(file=file)


@app.command(help_priority=3)
@click.option('-f', '--file', help='application yaml file', required=True)
@click.pass_context
def update(ctx, file):
    """ Update an ArgoCD application """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.update_application(json_file=file)


@app.command(help_priority=4)
@click.option('-n', '--name', help='application name', required=True)
@click.pass_context
def delete(ctx, name):
    """ Delete an ArgoCD application """
    from fd55.cli.argocd_client.argocd_cli import ArgoCD
    from fd55.utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.delete_application(application_name=name)
