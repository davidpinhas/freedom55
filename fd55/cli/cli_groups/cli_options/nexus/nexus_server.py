import click
from fd55.utils.cli_help_order import CliHelpOrder
from fd55.cli.nexus_client.nexus_cli import NexusRepositoryManager


@click.group(cls=CliHelpOrder)
@click.pass_context
def server(ctx):
    """ Nexus server commands """
    ctx.ensure_object(dict)


@server.command(help_priority=1)
@click.option('--id', help="task id", required=True)
@click.pass_context
def check_task_state(ctx, id):
    """ Check task state """
    NexusRepositoryManager().check_task_state(id=id)


@server.command(help_priority=2)
@click.pass_context
def run_backup_task(ctx):
    """ Run backup task """
    NexusRepositoryManager().run_backup_task()


@server.command(help_priority=3)
@click.pass_context
def run_repair_db_task(ctx):
    """ Run repair DB task """
    NexusRepositoryManager().run_repair_db_task()


@server.command(help_priority=4)
@click.pass_context
def list_repos(ctx):
    """ Retrieve repositories list """
    NexusRepositoryManager().list_repositories()


@server.command(help_priority=5)
@click.pass_context
def list_blob_store(ctx):
    """ Retrieve blob store information """
    NexusRepositoryManager().list_blob_stores()
