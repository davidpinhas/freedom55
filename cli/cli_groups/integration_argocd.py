import click
from cli.cli_groups.cli_options.argocd import argocd_app, argocd_repo, argocd_server


@click.group()
@click.pass_context
def argo(ctx):
    """ OCI Commands """
    ctx.ensure_object(dict)


argo.add_command(argocd_app.app)
argo.add_command(argocd_repo.repo)
argo.add_command(argocd_server.server)
