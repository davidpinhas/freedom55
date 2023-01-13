import click
from cli.cli_groups.cli_options.argocd import argocd_app, argocd_repo


@click.group()
@click.pass_context
def argo(ctx):
    """ OCI Commands """
    ctx.ensure_object(dict)


argo.add_command(argocd_app.app)
argo.add_command(argocd_repo.repo)