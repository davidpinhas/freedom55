import click
from cli.cli_groups.oci import oci
from cli.cli_groups.sops import sops
from cli.cli_groups.tf import tf
from cli.cli_groups.argocd import argo
from cli.cli_groups.cli_config import config


@click.group()
@click.option('-v', '--verbosity', default='info',
              help='Logging level (info, warn, error, debug)',
              required=False)
@click.version_option(version='2.6.1')
@click.pass_context
def main(ctx, verbosity):
    import logging
    from cli.functions import Functions as fn
    """Freedom 55 CLI.

        Freedom 55 - The operational client crafted by David Pinhas
        for maintaining, modifying, and operating your homelab."""
    ctx.ensure_object(dict)
    if verbosity == 'debug':
        log_level = logging.DEBUG
    elif verbosity == 'info':
        log_level = logging.INFO
    elif verbosity == 'warn':
        log_level = logging.WARNING
    elif verbosity == 'error':
        log_level = logging.ERROR
    else:
        logging.error("Wrong verbosity type")
        logging.error("Pick one of the available options: info, warn, error, debug")
        exit()
    fn.set_logger(log_level)

main.add_command(oci)
main.add_command(sops)
main.add_command(tf)
main.add_command(argo)
main.add_command(config)

if __name__ == '__main__':
    main(obj={})
