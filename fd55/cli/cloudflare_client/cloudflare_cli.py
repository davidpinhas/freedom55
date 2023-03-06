import requests
import json
import traceback
import logging
import CloudFlare
from prettytable import PrettyTable
from fd55.utils.fd55_config import Config
from fd55.utils.functions import Functions as fn
logger = logging.getLogger()
config = Config()


class Cloudflare:
    def __init__(self):
        blocked_domains = ['.cf', '.ga', '.gq', '.ml', '.tk']
        self.api_key = config.get('CLOUDFLARE', 'api_key')
        self.global_api_key = config.get('CLOUDFLARE', 'global_api_key')
        self.email = config.get('CLOUDFLARE', 'email')
        self.domain_name = config.get('CLOUDFLARE', 'domain_name')
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.zone_id = self.get_zone_id()
        self.cf = CloudFlare.CloudFlare(
            email=self.email, key=self.global_api_key)
        if any(self.domain_name.endswith(option)
               for option in blocked_domains):
            logging.error(
                "Cloudflare not supporting domains ending with '.cf, .ga, .gq, .ml, or .tk'")
            logging.warn(
                "This was a design desicion by Cloudflare to block free domains")
            logging.warn(
                "Read more here - https://community.cloudflare.com/t/unable-to-update-ddns-using-api-for-some-tlds/167228/11")
            exit()

    def set_default_headers(self):
        headers = {
            "X-Auth-Email": self.email,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        return headers

    def set_global_headers(self):
        headers = {
            "X-Auth-Email": self.email,
            "Authorization": f"Bearer {self.global_api_key}",
            "Content-Type": "application/json"
        }
        return headers

    def set_payload(
            comment=None,
            type=None,
            name=None,
            content=None,
            ttl=None,
            proxied=None):
        payload = {
            "comment": comment or "DNS record updated with Freedom 55",
            "type": type or "A",
            "name": name,
            "content": content,
            "ttl": ttl or 60,
            "proxied": proxied or False
        }
        logging.debug(f"Payload: {payload}")
        return payload

    def get_zone_id(self):
        """ Get zone ID """
        logging.debug(f"Retrieving zone ID")
        url = f"{self.base_url}/zones?name={self.domain_name}&status=active"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            records = json.loads(response.text)
            return records["result"][0]["id"]
        except Exception as e:
            logging.error(f"Failed to Get zone ID with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")

    def get_dns_record_id(self, name=None):
        """ Get DNS record ID """
        logging.info(f"Retrieving DNS record ID for {name}")
        url = f"{self.base_url}/zones/{self.zone_id}/dns_records"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            records = json.loads(response.text)
            for i in range(len(records["result"])):
                if records["result"][i]["name"] == f"{name}":
                    dns_record_id = records["result"][i]["id"]
                    dns_record_ip = records["result"][0]["content"]
                else:
                    pass
            if dns_record_id:
                return dns_record_id, dns_record_ip
        except Exception as e:
            logging.error(f"Failed to get DNS record ID with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")

    def list_dns_records(self, id=None):
        """ List DNS records """
        logging.info(f"Retrieving DNS records for domain '{self.domain_name}'")
        table = PrettyTable()
        url = f"{self.base_url}/zones/{self.zone_id}/dns_records"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            records = json.loads(response.text)
            for obj in range(len(records["result"])):
                dns_record = records['result'][obj]
                if id is not None:
                    table.field_names = [
                        'Name', 'Type', 'Content', 'TTL', 'Proxied', 'ID']
                    row = [
                        dns_record['name'],
                        dns_record['type'],
                        dns_record['content'],
                        dns_record['ttl'],
                        dns_record['proxied'],
                        dns_record['id']]
                else:
                    table.field_names = [
                        'Name', 'Type', 'Content', 'TTL', 'Proxied']
                    row = [
                        dns_record['name'],
                        dns_record['type'],
                        dns_record['content'],
                        dns_record['ttl'],
                        dns_record['proxied']
                    ]
                table.add_row(row)
            print(table)
        except Exception as e:
            logging.error(
                f"Failed to retrieve DNS records list with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")

    def create_dns_record(
            self,
            dns_zone_name,
            content,
            comment=None,
            type=None,
            ttl=None,
            proxied=None):
        """ Create DNS record """
        logging.info(f"Creating DNS record '{dns_zone_name}'")
        url = f"{self.base_url}/zones/{self.zone_id}/dns_records"
        payload = Cloudflare.set_payload(
            comment=comment,
            type=type,
            name=dns_zone_name,
            content=content,
            ttl=ttl,
            proxied=proxied)
        try:
            response = requests.request(
                "POST",
                url,
                headers=self.set_default_headers(),
                data=json.dumps(payload))
            records = json.loads(response.text)
            logging.info(f"New metadata for '{dns_zone_name}' record:")
            for key, value in records['result'].items():
                logging.info(f" * {key}: {value}")
        except Exception as e:
            logging.error(f"Failed to create DNS record with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")
            exit()
        logging.info(f"Finished modifying DNS record")

    def update_dns_record(
            self,
            dns_zone_name,
            content,
            comment=None,
            type=None,
            ttl=None,
            proxied=None):
        """ Update DNS record """
        logging.info(f"Updating DNS record '{dns_zone_name}'")
        dns_record_id, dns_record_ip = self.get_dns_record_id(
            name=dns_zone_name)
        url = f"{self.base_url}/zones/{self.zone_id}/dns_records/{dns_record_id}"
        payload = Cloudflare.set_payload(
            comment=comment,
            type=type,
            name=dns_zone_name,
            content=content,
            ttl=ttl,
            proxied=proxied)
        try:
            response = requests.put(
                url,
                headers=self.set_default_headers(),
                data=json.dumps(payload))
            records = json.loads(response.text)
            logging.info(f"New metadata for '{dns_zone_name}' record:")
            for key, value in records['result'].items():
                logging.info(f" * {key}: {value}")
        except Exception as e:
            logging.error(f"Failed to update DNS record with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")
            exit()
        logging.info(f"Finished modifying DNS record")

    def delete_dns_record(
            self,
            dns_zone_name):
        """ Delete DNS record """
        logging.info(f"Deleting DNS record '{dns_zone_name}'")
        dns_record_id, dns_record_ip = self.get_dns_record_id(
            name=dns_zone_name)
        url = f"{self.base_url}/zones/{self.zone_id}/dns_records/{dns_record_id}"
        try:
            response = requests.request(
                "DELETE", url, headers=self.set_default_headers())
            records = json.loads(response.text)
            logging.info(f"Finished deleting DNS record '{dns_zone_name}'")
        except Exception as e:
            logging.error(f"Failed to delete DNS record with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")
            exit()

    def list_waf_rules(self):
        """ List firewall rules """
        logging.info(
            f"Retrieving firewall rules for domain '{self.domain_name}'")
        table = PrettyTable()
        url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            firewall_rules = json.loads(response.text)
            for obj in range(len(firewall_rules["result"])):
                dns_record = firewall_rules['result'][obj]
                table.field_names = [
                    'ID', 'Description', 'Expression']
                row = [
                    dns_record['id'],
                    dns_record['description'],
                    dns_record['filter']['expression']
                ]
                table.add_row(row)
            print(table)
        except Exception as e:
            logging.error(
                f"Failed to retrieve firewall rules with error: {e}")
            logging.error(
                f"Request failed with error: {firewall_rules['errors']}")

    def list_waf_rule_filters(self):
        r = self.cf.zones.filters.get(self.zone_id)
        table = PrettyTable()
        for obj in r:
            table.field_names = ['ID', 'Expression']
            row = [obj['id'], obj['expression']]
            table.add_row(row)
        print(table)

    def create_waf_rule(
            self,
            name=None,
            action=None,
            expression=None,
            paused=False,
            description=None):
        """ Create firewall rules """
        logging.info(
            f"Creating firewall rule for domain '{self.domain_name}'")
        rule_filter = {
            'expression': f"({expression})",
            'paused': paused or False,
            'description': description or "No description provided",
        }
        rule_data = [
            {
                'action': action or "block",
                'filter': rule_filter,
                'description': name,
            }
        ]
        try:
            r = self.cf.zones.firewall.rules.post(self.zone_id, data=rule_data)
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            exit(1)
        logging.info(
            'Firewall rule created:\n' +
            json.dumps(
                r[0],
                indent=4,
                sort_keys=False) +
            '\n')

    def update_waf_rule(self,
                        id=None,
                        name=None,
                        action=None,
                        expression=None,
                        paused=False,
                        description=None):
        """ Update firewall rule """
        logging.info(f"Updating firewall rule for domain '{self.domain_name}'")
        try:
            rule = self.cf.zones.firewall.rules.get(
                self.zone_id, params={'id': id})
            rule_filter = {
                'id': rule[0]['filter']['id'],
                'expression': f"({expression})" or f"({rule[0]['filter']['expression']})",
                'paused': paused or False}
            if description:
                rule_filter['description'] = description
            rule_data = [
                {
                    'id': id or rule[0]['filter']['id'],
                    'action': action or rule[0]['filter']['action'],
                    'filter': rule_filter or rule[0]['filter']['rule_filter'],
                    'description': name or rule[0]['description']
                }
            ]
            if expression or paused or description:
                self.cf.zones.filters.put(
                    self.zone_id, rule[0]['filter']['id'], data=rule_filter)
            r = self.cf.zones.firewall.rules.put(
                self.zone_id, id, data=rule_data[0])
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            exit(1)
        logging.info(
            'Firewall rule updated:\n' +
            json.dumps(
                r,
                indent=4,
                sort_keys=False) +
            '\n')

    def delete_waf_rule(self, name=None, id=None):
        try:
            r = self.cf.zones.firewall.rules.get(self.zone_id)
            fn.modify_config_approval(
                f"Delete firewall rule and filter. Would you like to proceed? Y/n: ")
            for i in r:
                if name == i['description'] or id == i['id']:
                    deleted_rule = self.cf.zones.firewall.rules.delete(
                        self.zone_id, i['id'])
                    self.cf.zones.filters.delete(
                        self.zone_id, i['filter']['id'])
            logging.info('Deleted firewall rule with ID ' + deleted_rule['id'])
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            exit(1)

    def delete_waf_rule_filter(self, id=None):
        try:
            r = self.cf.zones.filters.get(self.zone_id)
            for i in r:
                if id == i['id']:
                    logging.info(f"Deleting firewall rule filter '{i['id']}'")
                    self.cf.zones.filters.delete(self.zone_id, i['id'])
                    logging.info(
                        f"Successfully deleted firewall rule filter with ID '{i['id']}'")
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            exit(1)