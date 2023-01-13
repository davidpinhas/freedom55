import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def repo(ctx):
    """ repository commands """
    ctx.ensure_object(dict)


@repo.command(help_priority=1)
@click.pass_context
def list(ctx):
    """ Lists ArgoCD repositories """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.list_repositories()


@repo.command(help_priority=2)
@click.option('-r', '--repo_url', help='Repository URL to add', required=True)
@click.option('-u', '--username', help='Repository username', required=False)
@click.option('-p', '--password', help='Repository password', required=False)
@click.pass_context
def add(ctx, repo_url, username=None, password=None):
    """ Add repository """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.add_repo(repo_url=repo_url, username=username, password=password)


@repo.command(help_priority=3)
@click.option('-r', '--repo_url', help='Repository URL to add', required=True)
@click.option('-u', '--username', help='Repository username', required=False)
@click.option('-p', '--password', help='Repository password', required=False)
@click.pass_context
def update(ctx, repo_url, username=None, password=None):
    """ Update repository """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.update_repo(repo_url=repo_url, username=username, password=password)


@repo.command(help_priority=4)
@click.option('-r', '--repo_url', help='Repository URL', required=True)
@click.pass_context
def delete(ctx, repo_url):
    """ Delete repository """
    from cli.argocd_client.argocd_cli import ArgoCD
    from utils.fd55_config import Config
    config = Config()
    argo = ArgoCD(
        api_endpoint=f"{config.get('ARGOCD', 'url')}",
        api_token=f"{str(config.get('ARGOCD', 'api_token'))}")
    argo.delete_repo(repo_url=repo_url)
