import click
from fd55.cli.cli_groups.cli_options.nexus import nexus_server


@click.group()
@click.pass_context
def nexus(ctx):
    """ Nexus Commands """
    ctx.ensure_object(dict)


nexus.add_command(nexus_server.server)
