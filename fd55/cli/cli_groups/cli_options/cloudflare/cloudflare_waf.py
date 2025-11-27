import click
import logging
from fd55.utils.cli_help_order import CliHelpOrder
from fd55.cli.cloudflare_client.cloudflare_cli import CloudflareClient
from fd55.utils.fd55_config import Config
from fd55.utils.functions import Functions as fn


@click.group(cls=CliHelpOrder)
@click.pass_context
def waf(ctx):
    """ Cloudflare WAF commands (Rulesets + Legacy) """
    ctx.ensure_object(dict)

    config = Config()
    if not config.get(section="CLOUDFLARE", option="global_api_key"):
        user_input = fn.modify_config_approval(
            "No global API key configured, configure now? Y/n: "
        )
        if user_input:
            input("Enter the value for global_api_key: ")


@waf.command(name="ruleset-list", help_priority=1)
@click.pass_context
def ruleset_list(ctx):
    """List all rulesets for the zone"""
    CloudflareClient().ruleset_list()


@waf.command(name="ruleset-get", help_priority=2)
@click.option('--id', required=True, help="Ruleset ID")
@click.pass_context
def ruleset_get(ctx, id):
    """Get a single ruleset"""
    CloudflareClient().ruleset_get(ruleset_id=id)


@waf.command(name="ruleset-update", help_priority=3)
@click.option('--id', required=True, help="Ruleset ID")
@click.option('--phase', required=False,
              help="Ruleset phase (e.g. http_request_firewall_custom)")
@click.option('--description', required=False, help="Ruleset description")
@click.pass_context
def ruleset_update(ctx, id, phase, description):
    """Update ruleset metadata"""
    CloudflareClient().ruleset_update(id=id, phase=phase, description=description)


@waf.command(name="ruleset-rule-add", help_priority=4)
@click.option('--ruleset-id', required=True, help="Ruleset ID")
@click.option('-n', '--name', required=True, help="Rule name")
@click.option('-a', '--action', default='block',
              help="Rule action (e.g. block, skip)")
@click.option('-e', '--expression', required=True, help="Rule expression")
@click.pass_context
def ruleset_rule_add(ctx, ruleset_id, name, action, expression):
    """Add a new rule to a ruleset"""
    CloudflareClient().ruleset_rule_add(
        ruleset_id=ruleset_id,
        name=name,
        action=action,
        expression=expression,
    )


@waf.command(name="ruleset-rule-update", help_priority=5)
@click.option('--ruleset-id', required=True, help="Ruleset ID")
@click.option('--rule-id', required=True, help="Rule ID inside the ruleset")
@click.option('-n', '--name', required=False, help="New rule name")
@click.option('-a', '--action', required=False, help="New rule action")
@click.option('-e', '--expression', required=False, help="New rule expression")
@click.pass_context
def ruleset_rule_update(ctx, ruleset_id, rule_id, name, action, expression):
    """Update a rule inside a ruleset"""
    CloudflareClient().ruleset_rule_update(
        ruleset_id=ruleset_id,
        rule_id=rule_id,
        name=name,
        action=action,
        expression=expression,
    )


@waf.command(name="ruleset-rule-delete", help_priority=6)
@click.option('--ruleset-id', required=True, help="Ruleset ID")
@click.option('--rule-id', required=True, help="Rule ID inside the ruleset")
@click.pass_context
def ruleset_rule_delete(ctx, ruleset_id, rule_id):
    """Delete a rule from a ruleset"""
    CloudflareClient().ruleset_rule_delete(
        ruleset_id=ruleset_id,
        rule_id=rule_id,
    )

# ============================================================
#  LEGACY FIREWALL RULES (DEPRECATED)
# ============================================================


@waf.command(name="old-list", help_priority=7)
@click.pass_context
def old_list(ctx):
    """[LEGACY] List firewall rules (deprecated by Cloudflare)"""
    CloudflareClient().list_waf_rules()


@waf.command(name="old-create", help_priority=8)
@click.option('-n', '--name', help='Rule name')
@click.option('-a', '--action', default='block', help='Action: allow/block')
@click.option('-e', '--expression', required=True, help='Filter expression')
@click.option('-p', '--paused', is_flag=True, default=False)
@click.option('-d', '--description', required=False)
@click.pass_context
def old_create(ctx, name, action, expression, paused, description):
    """[LEGACY] Create firewall rule"""
    CloudflareClient().create_waf_rule(
        name=name,
        action=action,
        expression=expression,
        paused=paused,
        description=description
    )


@waf.command(name="old-update", help_priority=9)
@click.option('--id', required=True, help='Rule ID')
@click.option('-n', '--name', help='Rule name')
@click.option('-a', '--action', default='block')
@click.option('-e', '--expression', required=True)
@click.option('-p', '--paused', is_flag=True, default=False)
@click.option('-d', '--description')
@click.pass_context
def old_update(ctx, id, name, action, expression, paused, description):
    """[LEGACY] Update firewall rule"""
    CloudflareClient().update_waf_rule(
        id=id,
        name=name,
        action=action,
        expression=expression,
        paused=paused,
        description=description
    )


@waf.command(name="old-delete", help_priority=10)
@click.option('-n', '--name', required=False)
@click.option('--id', required=False)
@click.pass_context
def old_delete(ctx, name, id):
    """[LEGACY] Delete firewall rule"""
    if not (name or id):
        logging.error("Requires --name or --id")
        return
    CloudflareClient().delete_waf_rule(name=name, id=id)


@waf.command(name="old-list-filters", help_priority=11)
@click.pass_context
def old_list_filters(ctx):
    """[DEPRECATED] Filters API removed"""
    CloudflareClient().list_waf_rule_filters()


@waf.command(name="old-delete-filter", help_priority=12)
@click.option('--id', required=True)
@click.pass_context
def old_delete_filter(ctx, id):
    """[DEPRECATED] Filters API removed"""
    CloudflareClient().delete_waf_rule_filter(id=id)
