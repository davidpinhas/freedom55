import click
from cli.cli_groups.cli_options.cloudflare import cloudflare_dns
from cli.cli_groups.cli_options.cloudflare import cloudflare_waf


@click.group()
@click.pass_context
def cf(ctx):
    """ Cloudflare Commands """
    ctx.ensure_object(dict)


cf.add_command(cloudflare_dns.dns)
cf.add_command(cloudflare_waf.waf)
