import requests
import json
import logging
from prettytable import PrettyTable
from utils.fd55_config import Config
logger = logging.getLogger()
config = Config()


class Cloudflare:
    def __init__(self):
        blocked_domains = ['.cf', '.ga', '.gq', '.ml', '.tk']
        self.api_key = config.get('CLOUDFLARE', 'api_key')
        self.email = config.get('CLOUDFLARE', 'email')
        self.domain_name = config.get('CLOUDFLARE', 'domain_name')
        self.headers = {
            "X-Auth-Email": self.email,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.cloudflare.com/client/v4"
        if any(self.domain_name.endswith(option)
               for option in blocked_domains):
            logging.error(
                "Cloudflare not supporting domains ending with '.cf, .ga, .gq, .ml, or .tk'")
            logging.warn(
                "This was a design desicion by Cloudflare to block free domains")
            logging.warn(
                "Read more here - https://community.cloudflare.com/t/unable-to-update-ddns-using-api-for-some-tlds/167228/11")
            exit()

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
            response = requests.get(url, headers=self.headers)
            records = json.loads(response.text)
            return records["result"][0]["id"]
        except Exception as e:
            logging.error(f"Failed to Get zone ID with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")

    def get_dns_record_id(self, name=None):
        """ Get DNS record ID """
        logging.info(f"Retrieving DNS record ID for {name}")
        zone_id = self.get_zone_id()
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        try:
            response = requests.get(url, headers=self.headers)
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
        zone_id = self.get_zone_id()
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        try:
            response = requests.get(url, headers=self.headers)
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
        zone_id = self.get_zone_id()
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        payload = Cloudflare.set_payload(
            comment=comment,
            type=type,
            name=dns_zone_name,
            content=content,
            ttl=ttl,
            proxied=proxied)
        try:
            response = requests.request(
                "POST", url, headers=self.headers, data=json.dumps(payload))
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
        zone_id = self.get_zone_id()
        dns_record_id, dns_record_ip = self.get_dns_record_id(
            name=dns_zone_name)
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{dns_record_id}"
        payload = Cloudflare.set_payload(
            comment=comment,
            type=type,
            name=dns_zone_name,
            content=content,
            ttl=ttl,
            proxied=proxied)
        try:
            response = requests.put(
                url, headers=self.headers, data=json.dumps(payload))
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
        zone_id = self.get_zone_id()
        dns_record_id, dns_record_ip = self.get_dns_record_id(
            name=dns_zone_name)
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{dns_record_id}"
        try:
            response = requests.request("DELETE",
                                        url, headers=self.headers)
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
        zone_id = self.get_zone_id()
        print(zone_id)
        url = f"{self.base_url}/zones/{zone_id}/firewall/rules"
        try:
            response = requests.get(url, headers=self.headers)
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