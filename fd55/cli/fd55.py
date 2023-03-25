import click
from fd55.cli.cli_groups.integration_oci import oci
from fd55.cli.cli_groups.integration_sops import sops
from fd55.cli.cli_groups.integration_tf import tf
from fd55.cli.cli_groups.integration_argocd import argo
from fd55.cli.cli_groups.integration_cli_config import config
from fd55.cli.cli_groups.integration_cloudflare import cf
from fd55.cli.cli_groups.integration_ai import ai


@click.group()
@click.option('-v', '--verbosity', default='info',
              help='Logging level (info, warn, error, debug)',
              required=False)
@click.version_option(version='3.4.8')
@click.pass_context
def main(ctx, verbosity):
    import logging
    from fd55.utils.functions import Functions as fn
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
        logging.error(
            "Pick one of the available options: info, warn, error, debug")
        exit()
    fn.set_logger(log_level)


main.add_command(oci)
main.add_command(sops)
main.add_command(tf)
main.add_command(argo)
main.add_command(cf)
main.add_command(config)
main.add_command(ai)

if __name__ == '__main__':
    main(obj={})
