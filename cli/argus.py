import click
import logging
from cli.cli_groups.oci import oci
from cli.cli_groups.sops import sops
from cli.cli_groups.tf import tf
from cli.cli_groups.argocd import argo

@click.group()
@click.option('--log', default='INFO',
              help='Logging level (INFO, WARNING, ERROR, CRITICAL, DEBUG)',
              required=False)
@click.pass_context
def main(ctx, log):
    """Argus CLI tools.

        The Argus CLI is an operational tool crafted by David Pinhas
        To maintain, modify and operate a homelab."""
    ctx.ensure_object(dict)
    pass


main.add_command(oci)
main.add_command(sops)
main.add_command(tf)
main.add_command(argo)

if __name__ == '__main__':
    main(obj={})
