import requests
import json
import yaml
import traceback
import logging
from cloudflare import Cloudflare
from retry import retry
from prettytable import PrettyTable
from fd55.utils.fd55_config import Config
from fd55.utils.functions import Functions as fn
logger = logging.getLogger()
config = Config()


class CloudflareClient:
    def __init__(self):
        blocked_domains = ['.cf', '.ga', '.gq', '.ml', '.tk']
        self.api_key = config.get('CLOUDFLARE', 'api_key')
        self.global_api_key = config.get('CLOUDFLARE', 'global_api_key')
        self.email = config.get('CLOUDFLARE', 'email')
        self.domain_name = config.get('CLOUDFLARE', 'domain_name')
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.zone_id = self.get_zone_id()
        self.cf = Cloudflare(api_key=self.global_api_key, api_email=self.email)
        if any(self.domain_name.endswith(option)
               for option in blocked_domains):
            logging.error(
                "Cloudflare not supporting domains ending with '.cf, .ga, .gq, .ml, or .tk'")
            logging.warning(
                "This was a design desicion by Cloudflare to block free domains")
            logging.warning(
                "Read more here - https://community.cloudflare.com/t/unable-to-update-ddns-using-api-for-some-tlds/167228/11")
            exit()

    def set_default_headers(self):
        """ Set default request headers """
        headers = {
            "X-Auth-Email": self.email,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        return headers

    def set_global_headers(self):
        """ Set global request headers """
        headers = {
            "X-Auth-Email": self.email,
            "Authorization": f"Bearer {self.global_api_key}",
            "Content-Type": "application/json"
        }
        return headers

    def set_payload(
            self,
            comment=None,
            type=None,
            name=None,
            content=None,
            ttl=None,
            proxied=None):
        """ Create payload """
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

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
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

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
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

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def list_dns_records(self, id=None):
        """ List DNS records """
        url = f"{self.base_url}/zones/{self.zone_id}/dns_records"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            records = json.loads(response.text)
            if records.get('errors'):
                logging.error(
                    f"Request failed with error: {records.get('errors')}")
                return
            print(json.dumps(records["result"], indent=2))
        except Exception as e:
            logging.error(
                f"Failed to retrieve DNS records list with error: {e}")
            raise e

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
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
        payload = self.set_payload(
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
            raise e
        logging.info(f"Finished modifying DNS record")

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
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
        try:
            dns_record_id, dns_record_ip = self.get_dns_record_id(
                name=dns_zone_name)
            if not dns_record_id:
                logging.error(
                    f"DNS record ID for '{dns_zone_name}' could not be found.")
                raise ValueError(f"No DNS record found for '{dns_zone_name}'")
            url = f"{self.base_url}/zones/{self.zone_id}/dns_records/{dns_record_id}"
            payload = self.set_payload(
                comment=comment,
                type=type,
                name=dns_zone_name,
                content=content,
                ttl=ttl,
                proxied=proxied
            )
            response = requests.put(
                url,
                headers=self.set_default_headers(),
                data=json.dumps(payload)
            )
            if response.status_code != 200:
                logging.error(
                    f"Failed to update DNS record '{dns_zone_name}'.")
                response_data = response.json()
                errors = response_data.get("errors", [])
                for error in errors:
                    logging.error(
                        f"Error {error.get('code')}: {error.get('message')}")
                raise Exception("DNS record update failed due to API errors.")
            records = response.json()
            logging.info(f"New metadata for '{dns_zone_name}' record:")
            for key, value in records['result'].items():
                logging.info(f" * {key}: {value}")
            logging.info(f"Successfully updated DNS record '{dns_zone_name}'")
        except Exception as e:
            logging.error(f"Failed to update DNS record: {e}")
            raise

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
            raise e

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def list_waf_rules(self):
        """ List firewall rules """
        url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            firewall_rules = json.loads(response.text)
            if firewall_rules.get('errors'):
                logging.error(
                    f"Request failed with error: {firewall_rules.get('errors')}")
                return
            print(json.dumps(firewall_rules["result"], indent=2))
        except Exception as e:
            logging.error(f"Failed to retrieve firewall rules with error: {e}")
            raise e

    def list_waf_rule_filters(self):
        """ List firewall rules filters """
        url = f"{self.base_url}/zones/{self.zone_id}/filters"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            filters_data = json.loads(response.text)
            if filters_data.get('errors'):
                logging.error(
                    f"Request failed with error: {filters_data.get('errors')}")
                return
            filters_list = [{'id': f.get('id'), 'expression': f.get(
                'expression')} for f in filters_data.get('result', [])]
            print(json.dumps(filters_list, indent=2))
        except Exception as e:
            logging.error(
                f"Failed to retrieve firewall rule filters with error: {e}")
            raise e

    def _model_to_dict(self, obj):
        """ Convert model object to dict """
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()
        if hasattr(obj, 'dict'):
            return obj.dict()
        return obj

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def create_waf_rule(
            self,
            name=None,
            action=None,
            expression=None,
            paused=False,
            description=None):
        """ Create firewall rules """
        logging.info(f"Creating firewall rule for domain '{self.domain_name}'")
        try:
            filter_payload = {
                'expression': f"({expression})",
                'paused': paused}
            if description:
                filter_payload['description'] = description or "No description provided"
            filter_url = f"{self.base_url}/zones/{self.zone_id}/filters"
            filter_response = requests.post(
                filter_url,
                headers=self.set_default_headers(),
                data=json.dumps(filter_payload))
            filter_data = json.loads(filter_response.text)
            if filter_response.status_code != 200:
                raise Exception(
                    f"Failed to create filter: {filter_data.get('errors', [])}")
            filter_id = filter_data['result'][0]['id']
            rule_payload = {
                'action': action or "block",
                'filter': {'id': filter_id}
            }
            if name:
                rule_payload['description'] = name
            rule_url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules"
            rule_response = requests.post(
                rule_url,
                headers=self.set_default_headers(),
                data=json.dumps(
                    [rule_payload]))
            rule_data = json.loads(rule_response.text)
            if rule_response.status_code != 200:
                raise Exception(
                    f"Failed to create firewall rule: {rule_data.get('errors', [])}")
            logging.info(
                f'Firewall rule created:\n{json.dumps(rule_data["result"][0], indent=4, sort_keys=False, default=str)}\n')
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            raise e

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def update_waf_rule(
            self,
            id=None,
            name=None,
            action=None,
            expression=None,
            paused=False,
            description=None):
        """ Update firewall rule """
        logging.info(f"Updating firewall rule for domain '{self.domain_name}'")
        try:
            rule = self.cf.firewall.rules.get(rule_id=id, zone_id=self.zone_id)
            filter_id = rule.filter.id
            filter_update_body = {}
            if expression:
                filter_update_body['expression'] = f"({expression})"
            if paused is not False:
                filter_update_body['paused'] = paused
            if description:
                filter_update_body['description'] = description
            if filter_update_body:
                self.cf.filters.update(
                    filter_id=filter_id,
                    zone_id=self.zone_id,
                    body=filter_update_body)
            rule_params = {
                'rule_id': id,
                'zone_id': self.zone_id,
                'action': action or rule.action,
                'filter': {'id': filter_id}
            }
            if name:
                rule_params['description'] = name
            updated_rule = self.cf.firewall.rules.update(**rule_params)
            logging.info(
                f'Firewall rule updated:\n{json.dumps(self._model_to_dict(updated_rule), indent=4, sort_keys=False, default=str)}\n')
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            raise e

    def delete_waf_rule(self, name=None, id=None):
        """ Delete firewall rule """
        try:
            url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules"
            response = requests.get(url, headers=self.set_default_headers())
            firewall_rules = json.loads(response.text)
            logging.warning("Deleting firewall rule and filter")
            fn.modify_config_approval(f"Would you like to proceed? Y/n: ")
            for rule in firewall_rules.get("result", []):
                if name == rule.get('description') or id == rule.get('id'):
                    rule_id = rule.get('id')
                    delete_url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules/{rule_id}"
                    delete_response = requests.delete(
                        delete_url, headers=self.set_default_headers())
                    if delete_response.status_code == 200:
                        logging.info(
                            f'Deleted firewall rule with ID {rule_id}')
                    else:
                        logging.error(
                            f'Failed to delete firewall rule: {delete_response.text}')
                    return
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            raise e

    def delete_waf_rule_filter(self, id=None):
        """ Delete firewall rule filter (deprecated - Filters API is deprecated) """
        logging.error(
            "Filters API is deprecated. To delete a filter, delete the associated firewall rule instead.")
        logging.info(
            "Listing firewall rules to find the rule associated with this filter...")
        try:
            url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules"
            response = requests.get(url, headers=self.set_default_headers())
            firewall_rules = json.loads(response.text)
            for rule in firewall_rules.get("result", []):
                filter_id = rule.get('filter', {}).get('id')
                if filter_id == id:
                    rule_id = rule.get('id')
                    logging.info(
                        f"Found firewall rule '{rule_id}' using filter '{id}'. Delete the rule to remove the filter.")
                    logging.info(f"Use: fd55 cf waf delete --id {rule_id}")
                    return
            logging.warning(f"No firewall rule found using filter ID '{id}'")
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            raise e
