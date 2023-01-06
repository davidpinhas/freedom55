import requests
import json
import logging
logger = logging.getLogger()


class Cloudflare:
    def __init__(self, api_key, email, domain_name):
        self.api_key = api_key
        self.email = email
        self.domain_name = domain_name
        self.headers = {
            "X-Auth-Email": self.email,
            "X-Auth-Key": self.api_key,
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.cloudflare.com/client/v4"

    def get_zone_id(self):
        """ Get zone ID """
        url = f"{self.base_url}/zones?name={self.domain_name}&status=active"
        try:
            response = requests.get(url, headers=self.headers)
            data = json.loads(response.text)
            return data["result"][0]["id"]
        except Exception as e:
            logging.error(f"Failed to update DNS record with error '{e}'")

    def get_dns_record_id(self, name=None):
        """ Get DNS record ID """
        zone_id = self.get_zone_id()
        url = f"{self.base_url}/zones/{zone_id}/dns_records/"
        try:
            response = requests.get(url, headers=self.headers)
            data = json.loads(response.text)
            for i in range(len(data["result"])):
                if data["result"][i]["name"] == f"{name}":
                    dns_record_id = data['result'][i]['id']
                    dns_record_ip = data['result'][0]["content"]
                else:
                    pass
            if dns_record_id:
                return dns_record_id, dns_record_ip
        except Exception as e:
            logging.error(f"Failed to update DNS record with error '{e}'")

    def update_dns_record(
            self,
            dns_zone_name,
            type=None,
            ttl=None,
            proxied=None):
        """ Update DNS record """
        logging.info(f"Updating DNS record '{dns_zone_name}'")
        zone_id = self.get_zone_id()
        dns_record_id, dns_record_ip = self.get_dns_record_id(
            name=dns_zone_name)
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{dns_record_id}"
        payload = {
            "type": type or "A",
            "name": dns_zone_name,
            "content": dns_record_ip,
            "ttl": ttl or 60,
            "proxied": proxied or False
        }
        try:
            response = requests.put(
                url, headers=self.headers, data=json.dumps(payload))
            data = json.loads(response.text)
            return data
        except Exception as e:
            logging.error(f"Failed to update DNS record with error '{e}'")
