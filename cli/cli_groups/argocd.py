import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def argo(ctx):
    """ ArgoCD commands """
    ctx.ensure_object(dict)


@argo.command(help_priority=1)
@click.pass_context
def get_apps(ctx):
    """ Get ArgoCD applications """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.get_applications()


@argo.command(help_priority=2)
@click.option('-f', '--file', help='application yaml file', required=True)
@click.pass_context
def create_app(ctx, file):
    """ Create an ArgoCD application """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.create_application(json_file=file)


@argo.command(help_priority=3)
@click.option('-f', '--file', help='application yaml file', required=True)
@click.pass_context
def update_app(ctx, file):
    """ Update an ArgoCD application """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.update_application(json_file=file)


@argo.command(help_priority=4)
@click.option('-n', '--name', help='application name', required=True)
@click.pass_context
def delete_app(ctx, name):
    """ Delete an ArgoCD application """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.delete_application(application_name=name)


@argo.command(help_priority=5)
@click.pass_context
def list_repos(ctx):
    """ Lists ArgoCD repositories """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.list_repositories()

@argo.command(help_priority=6)
@click.option('-r', '--repo_url', help='Repository URL to add', required=True)
@click.option('-u', '--username', help='Repository username', required=False)
@click.option('-p', '--password', help='Repository password', required=False)
@click.pass_context
def add_repo(ctx, repo_url, username=None, password=None):
    """ Add repository """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.add_repo(repo_url=repo_url, username=username, password=password)

@argo.command(help_priority=7)
@click.option('-r', '--repo_url', help='Repository URL to add', required=True)
@click.option('-u', '--username', help='Repository username', required=False)
@click.option('-p', '--password', help='Repository password', required=False)
@click.pass_context
def update_repo(ctx, repo_url, username=None, password=None):
    """ Update repository """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.update_repo(repo_url=repo_url, username=username, password=password)

@argo.command(help_priority=8)
@click.option('-r', '--repo_url', help='Repository URL', required=True)
@click.pass_context
def delete_repo(ctx, repo_url):
    """ Delete repository """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.delete_repo(repo_url=repo_url)
