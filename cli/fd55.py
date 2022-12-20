import click
import logging
from cli.cli_groups.oci import oci
from cli.cli_groups.sops import sops
from cli.cli_groups.tf import tf
from cli.cli_groups.argocd import argo
from cli.functions import Functions as fn
import re

with open('setup.py', 'r') as f:
    setup_py = f.read()
version = re.search(r'version=([\'"])([^\'"]+)\1', setup_py).group(2)

@click.group()
@click.option('-v', '--verbosity', default='info',
              help='Logging level (info, warn, error, debug)',
              required=False)
@click.version_option(version=version)
@click.pass_context
def main(ctx, verbosity):
    """Freedom 55 CLI tools.

        The freedom 55 CLI is an operational tool crafted by David Pinhas
        To maintain, modify and operate a homelab."""
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

if __name__ == '__main__':
    main(obj={})