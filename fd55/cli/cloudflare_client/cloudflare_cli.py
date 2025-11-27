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

    def _sanitize(self, obj):
        """Recursively convert datetimes and unsupported types to JSON-serializable objects."""
        if isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._sanitize(i) for i in obj]
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        return obj

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
            self,
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

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def get_zone_id(self):
        logging.debug("Retrieving zone ID")
        url = f"{self.base_url}/zones?name={self.domain_name}&status=active"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            records = json.loads(response.text)
            return records["result"][0]["id"]
        except Exception as e:
            logging.error(f"Failed to Get zone ID with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")
            raise

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def get_dns_record_id(self, name=None):
        logging.info(f"Retrieving DNS record ID for {name}")
        url = f"{self.base_url}/zones/{self.zone_id}/dns_records"
        try:
            response = requests.get(url, headers=self.set_default_headers())
            records = json.loads(response.text)
            dns_record_id = None
            dns_record_ip = None
            for i in range(len(records["result"])):
                if records["result"][i]["name"] == f"{name}":
                    dns_record_id = records["result"][i]["id"]
                    dns_record_ip = records["result"][i]["content"]
            if dns_record_id:
                return dns_record_id, dns_record_ip
        except Exception as e:
            logging.error(f"Failed to get DNS record ID with error: {e}")
            logging.error(f"Request failed with error: {records['errors']}")
            raise

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def list_dns_records(self, id=None):
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
            raise

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
            raise
        logging.info("Finished modifying DNS record")

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
            raise

    @retry(exceptions=(Exception,), tries=3,
           delay=1, backoff=2, logger=logging)
    def list_waf_rules(self):
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
            raise

    def list_waf_rule_filters(self):
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
            raise

    def _model_to_dict(self, obj):
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
        logging.info(f"Creating firewall rule for domain '{self.domain_name}'")
        try:
            filter_payload = {
                'expression': f"({expression})" if expression else '',
                'paused': paused
            }
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
                f"Firewall rule created:\n{json.dumps(rule_data['result'][0], indent=4, sort_keys=False, default=str)}\n")
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            raise

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
        logging.info(f"Updating firewall rule for domain '{self.domain_name}'")
        try:
            if not id:
                raise ValueError("Rule id is required")
            rule_url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules/{id}"
            rule_resp = requests.get(
                rule_url, headers=self.set_default_headers())
            rule_data = rule_resp.json()
            if rule_resp.status_code != 200:
                raise Exception(rule_data.get('errors', []))
            rule = rule_data.get('result', {})
            filter_id = rule.get('filter', {}).get('id')
            if not filter_id:
                raise ValueError(f"No filter associated with rule '{id}'")
            filter_body = {}
            if expression:
                filter_body['expression'] = f"({expression})"
            if description:
                filter_body['description'] = description
            if paused is not False:
                filter_body['paused'] = paused
            if filter_body:
                filter_url = f"{self.base_url}/zones/{self.zone_id}/filters/{filter_id}"
                f_resp = requests.put(
                    filter_url,
                    headers=self.set_default_headers(),
                    data=json.dumps(filter_body)
                )
                f_data = f_resp.json()
                if f_resp.status_code != 200:
                    raise Exception(f_data.get('errors', []))
            rule_body = {}
            if action:
                rule_body['action'] = action
            if name:
                rule_body['description'] = name
            if paused is not False:
                rule_body['paused'] = paused
            if rule_body:
                r_resp = requests.put(
                    rule_url,
                    headers=self.set_default_headers(),
                    data=json.dumps(rule_body)
                )
                r_data = r_resp.json()
                if r_resp.status_code != 200:
                    raise Exception(r_data.get('errors', []))
                logging.info(
                    f"Firewall rule updated:\n{json.dumps(r_data.get('result', {}), indent=4, sort_keys=False, default=str)}\n")
            else:
                logging.info("No changes applied to firewall rule")
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            raise

    def delete_waf_rule(self, name=None, id=None):
        try:
            url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules"
            response = requests.get(url, headers=self.set_default_headers())
            firewall_rules = json.loads(response.text)
            logging.warning("Deleting firewall rule and filter")
            fn.modify_config_approval("Would you like to proceed? Y/n: ")
            for rule in firewall_rules.get("result", []):
                if name == rule.get('description') or id == rule.get('id'):
                    rule_id = rule.get('id')
                    filter_id = rule.get('filter', {}).get('id')
                    delete_url = f"{self.base_url}/zones/{self.zone_id}/firewall/rules/{rule_id}"
                    delete_response = requests.delete(
                        delete_url, headers=self.set_default_headers())
                    if delete_response.status_code == 200:
                        logging.info(
                            f"Deleted firewall rule with ID {rule_id}")
                    else:
                        logging.error(
                            f"Failed to delete firewall rule: {delete_response.text}")
                    if filter_id:
                        f_url = f"{self.base_url}/zones/{self.zone_id}/filters/{filter_id}"
                        f_resp = requests.delete(
                            f_url, headers=self.set_default_headers())
                        if f_resp.status_code == 200:
                            logging.info(f"Deleted filter with ID {filter_id}")
                        else:
                            logging.error(
                                f"Failed to delete filter: {f_resp.text}")
                    return
        except Exception as e:
            logging.error(f"Failed with error: '{e}'")
            logging.error(traceback.format_exc())
            raise

    def delete_waf_rule_filter(self, id=None):
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
            raise

    def ruleset_list(self):
        try:
            rulesets = self.cf.rulesets.list(zone_id=self.zone_id)
            print(json.dumps([rs.model_dump()
                              for rs in rulesets], indent=2, default=str))
        except Exception as e:
            logging.error(f"Failed to list rulesets: {e}")
            raise

    def ruleset_get(self, ruleset_id):
        try:
            rs = self.cf.rulesets.get(
                zone_id=self.zone_id, ruleset_id=ruleset_id)
            print(json.dumps(rs.model_dump(), indent=2, default=str))
        except Exception as e:
            logging.error(f"Failed to fetch ruleset '{ruleset_id}': {e}")
            raise

    def ruleset_rule_add(self, ruleset_id, name, action, expression):
        try:
            rs = self.cf.rulesets.get(
                zone_id=self.zone_id, ruleset_id=ruleset_id)
            updated = rs.model_dump()

            new_rule = {
                "action": action,
                "description": name,
                "expression": expression,
                "enabled": True
            }

            updated["rules"].append(new_rule)

            result = self.cf.rulesets.update(
                zone_id=self.zone_id,
                ruleset_id=ruleset_id,
                body=updated
            )

            print(json.dumps(result.model_dump(), indent=2, default=str))

        except Exception as e:
            logging.error(f"Failed to add rule to ruleset '{ruleset_id}': {e}")
            raise

    def ruleset_rule_update(
            self,
            ruleset_id,
            rule_id,
            name=None,
            action=None,
            expression=None):
        try:
            # 1. Fetch the ruleset
            rs = self.cf.rulesets.get(
                zone_id=self.zone_id, ruleset_id=ruleset_id)
            updated = rs.model_dump()

            # 2. Modify the desired rule
            found = False
            for r in updated["rules"]:
                if r["id"] == rule_id:
                    found = True
                    if name:
                        r["description"] = name
                    if action:
                        r["action"] = action
                    if expression:
                        r["expression"] = expression

            if not found:
                raise ValueError(f"Rule '{rule_id}' not found")

            # 3. Sanitize (remove datetimes)
            sanitized = self._sanitize(updated)

            # 4. Perform RAW PATCH request
            url = f"{self.base_url}/zones/{self.zone_id}/rulesets/{ruleset_id}"
            headers = self.set_global_headers()
            response = requests.patch(
                url, headers=headers, data=json.dumps(sanitized))
            result = response.json()

            if response.status_code not in (200, 201):
                raise Exception(result)

            print(json.dumps(result, indent=2))

        except Exception as e:
            logging.error(
                f"Failed to update rule '{rule_id}' in ruleset '{ruleset_id}': {e}")
            raise

    def ruleset_rule_delete(self, ruleset_id, rule_id):
        try:
            rs = self.cf.rulesets.get(
                zone_id=self.zone_id, ruleset_id=ruleset_id)
            updated = rs.model_dump()

            before = len(updated["rules"])
            updated["rules"] = [
                r for r in updated["rules"] if r["id"] != rule_id]

            if len(updated["rules"]) == before:
                raise ValueError(f"Rule '{rule_id}' not found")

            result = self.cf.rulesets.update(
                zone_id=self.zone_id,
                ruleset_id=ruleset_id,
                body=updated
            )

            print(json.dumps(result.model_dump(), indent=2, default=str))

        except Exception as e:
            logging.error(
                f"Failed to delete rule '{rule_id}' from ruleset '{ruleset_id}': {e}")
            raise
