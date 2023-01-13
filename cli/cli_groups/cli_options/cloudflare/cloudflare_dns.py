import click
from utils.cli_help_order import CliHelpOrder
from cli.cloudflare_client.cloudflare_cli import Cloudflare


@click.group(cls=CliHelpOrder)
@click.pass_context
def dns(ctx):
    """ Cloudflare commands """
    ctx.ensure_object(dict)


@dns.command(help_priority=1)
@click.option('--id',
              help='Get ID with records list',
              is_flag=True)
@click.pass_context
def list(ctx, id):
    """ List DNS records """
    if id:
        Cloudflare().list_dns_records(id=True)
    else:
        Cloudflare().list_dns_records()


@dns.command(help_priority=2)
@click.option('-n',
              '--name',
              help='DNS name. Ex: sub.domain.com',
              required=True)
@click.option('-c',
              '--content',
              help='Target address content, can set IP or domain name. Ex: 123.123.123.123 or domain.com',
              required=True)
@click.option('-t',
              '--type',
              help='DNS record type, if not set, "A" record will be used',
              default="A",
              required=False)
@click.option('--ttl',
              help='Time to live.',
              default=60,
              required=False)
@click.option('--comment',
              help='Record comment',
              required=False)
@click.option('-p',
              '--proxied',
              help='Set proxy to TRUE',
              is_flag=True)
@click.pass_context
def create(ctx, name, content, type, ttl, comment, proxied):
    """ Create DNS record """
    Cloudflare().create_dns_record(
        dns_zone_name=name,
        content=content,
        type=type,
        ttl=ttl,
        comment=comment,
        proxied=proxied)


@dns.command(help_priority=3)
@click.option('-n',
              '--name',
              help='DNS name. Ex: sub.domain.com',
              required=True)
@click.option('-c',
              '--content',
              help='Target address content, can set IP or domain name. Ex: 123.123.123.123 or domain.com',
              required=True)
@click.option('-t',
              '--type',
              help='DNS record type, if not set, "A" record will be used',
              default="A",
              required=False)
@click.option('--ttl',
              help='Time to live.',
              default=60,
              required=False)
@click.option('--comment',
              help='Record comment',
              required=False)
@click.option('-p',
              '--proxied',
              help='Set proxy to TRUE',
              is_flag=True)
@click.pass_context
def update(ctx, name, content, type, ttl, comment, proxied):
    """ Update DNS record """
    Cloudflare().update_dns_record(
        dns_zone_name=name,
        content=content,
        type=type,
        ttl=ttl,
        comment=comment,
        proxied=proxied)


@dns.command(help_priority=4)
@click.option('-n',
              '--name',
              help='DNS name. Ex: sub.domain.com',
              required=True)
@click.pass_context
def delete(ctx, name):
    """ Update DNS record """
    Cloudflare().delete_dns_record(dns_zone_name=name)
