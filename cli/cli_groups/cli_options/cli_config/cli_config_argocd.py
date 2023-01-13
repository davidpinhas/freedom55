import click
import logging
from utils.fd55_config import Config


@click.group()
@click.pass_context
def argo(ctx):
    """ Configure ArgoCD """
    ctx.ensure_object(dict)


@argo.command()
@click.option('-u', '--url', help='ArgoCD base URL', required=False)
@click.option('-p', '--api_token', help='ArgoCD Token', required=False)
@click.pass_context
def set(ctx, url=None, api_token=None):
    """ Set ArgoCD keys """
    config = Config()
    if url:
        config.create_option("ARGOCD", "url", url)
    if api_token:
        config.create_option("ARGOCD", "api_token", api_token)
    if not any([url, api_token]):
        logging.warning("At least one parameter is required.")
