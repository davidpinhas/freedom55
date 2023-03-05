import click
import logging
from fd55.utils.fd55_config import Config


@click.group()
@click.pass_context
def oci(ctx=None):
    """ Configure Oracle Cloud Infrastructure """
    ctx.ensure_object(dict)


@oci.command()
@click.option('-u', '--user', help='OCI user', required=False)
@click.option('-f',
              '--fingerprint',
              help='OCI account fingerprint',
              required=False)
@click.option('-t', '--tenancy', help='OCI account tenancy', required=False)
@click.option('-r', '--region', help='OCI account region', required=False)
@click.option('-k', '--key-file', help='OCI key file', required=False)
@click.pass_context
def set(
        ctx,
        user=None,
        fingerprint=None,
        tenancy=None,
        region=None,
        key_file=None):
    """ Set OCI keys """
    config = Config()
    if user:
        config.create_option("OCI", "user", user)
    if fingerprint:
        config.create_option("OCI", "fingerprint", fingerprint)
    if tenancy:
        config.create_option("OCI", "tenancy", tenancy)
    if region:
        config.create_option("OCI", "region", region)
    if key_file:
        config.create_option("OCI", "key_file", key_file)
    if not any([user, fingerprint, tenancy, region, key_file]):
        logging.warning("At least one parameter is required.")
