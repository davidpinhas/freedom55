import click
from utils.cli_help_order import CliHelpOrder


@click.group(cls=CliHelpOrder)
@click.pass_context
def waf(ctx):
    """ OCI firewall related commands """
    ctx.ensure_object(dict)


@waf.command(help_priority=1)
@click.option('--id', help="Set the description", is_flag=True)
@click.pass_context
def list_nsg(ctx, id=None):
    """ List load balancer NSG """
    from cli.oci_client.oci_cli import Oci
    if id:
        Oci.list_lb_nsg(id=True)
    else:
        Oci.list_lb_nsg()


@waf.command(help_priority=2)
@click.option('--id', help="Set network security group ID", required=True)
@click.pass_context
def list_nsg_rules(ctx, id=None):
    """ List load balancer NSG rules """
    from cli.oci_client.oci_cli import Oci
    Oci.list_lb_nsg_rules(id=id)


@waf.command(help_priority=3)
@click.option('--id', help="Set NSG ID", required=True)
@click.option('--rule-id', help="Set NSG rule ID", required=True)
@click.option('--protocol', help="Set the protocol", required=True)
@click.option('--direction', help="Set the direction", required=True)
@click.option('--description', help="Set the description", required=False)
@click.option('--destination', help="Set the destination", required=False)
@click.option('--destination-type',
              help="Set the destination type",
              required=False)
@click.option('--icmp-type', help="Set the ICMP type", required=False)
@click.option('--icmp-code', help="Set the ICMP code", required=False)
@click.option('--is-stateless',
              help="Set if the rule is stateless",
              required=False)
@click.option('--source', help="Set the source", required=False)
@click.option('--source-type', help="Set the source type", required=False)
@click.option('--tcp-destination-min',
              help="Set the TCP destination minimum port",
              required=False)
@click.option('--tcp-destination-max',
              help="Set the TCP destination maximum port",
              required=False)
@click.option('--tcp-source-min',
              help="Set the TCP source minimum port",
              required=False)
@click.option('--tcp-source-max',
              help="Set the TCP source maximum port",
              required=False)
@click.option('--udp-destination-min',
              help="Set the UDP destination minimum port",
              required=False)
@click.option('--udp-destination-max',
              help="Set the UDP destination maximum port",
              required=False)
@click.option('--udp-source-min',
              help="Set the UDP source minimum port",
              required=False)
@click.option('--udp-source-max',
              help="Set the UDP source maximum port",
              required=False)
@click.pass_context
def update_nsg_rule(
        ctx,
        id=None,
        rule_id=None,
        protocol=None,
        direction=None,
        description=None,
        destination=None,
        destination_type=None,
        icmp_type=None,
        icmp_code=None,
        is_stateless=None,
        source=None,
        source_type=None,
        tcp_destination_min=None,
        tcp_destination_max=None,
        tcp_source_min=None,
        tcp_source_max=None,
        udp_destination_min=None,
        udp_destination_max=None,
        udp_source_min=None,
        udp_source_max=None):
    """ update load balancer NSG rule """
    from cli.oci_client.oci_cli import Oci
    Oci.update_lb_nsg_rule(
        id=id,
        rule_id=rule_id,
        protocol=protocol,
        direction=direction,
        description=description,
        destination=destination,
        destination_type=destination_type,
        icmp_type=icmp_type,
        icmp_code=icmp_code,
        is_stateless=is_stateless,
        source=source,
        source_type=source_type,
        tcp_destination_min=tcp_destination_min,
        tcp_destination_max=tcp_destination_max,
        tcp_source_min=tcp_source_min,
        tcp_source_max=tcp_source_max,
        udp_destination_min=udp_destination_min,
        udp_destination_max=udp_destination_max,
        udp_source_min=udp_source_min,
        udp_source_max=udp_source_max)
