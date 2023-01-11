import requests
from prettytable import PrettyTable
from utils.fd55_config import Config
from cli.functions import Functions as fn
import json
import logging
logger = logging.getLogger()

config = Config()


class ArgoCD:
    def __init__(self, api_endpoint, api_token):
        self.api_endpoint = api_endpoint
        self.api_token = api_token

    def request(self, uri=None, method="GET", data=None, headers=None):
        if uri is not None:
            url = f"{self.api_endpoint}/{uri}"
        else:
            url = f"{self.api_endpoint}/api/v1/applications"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        if data is not None:
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            response = requests.request(
                url=url, method=method, headers=headers, json=data)
        else:
            response = requests.request(
                url=url, method=method, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to execute: {logging.error(response.text)}")
        logging.debug(response.text)
        json_output = response.json()
        return json.dumps(json_output, indent=4)

    def get_applications(self):
        """ Get all ArgoCD applications """
        logging.info("Getting ArgoCD applications")
        argo = ArgoCD(api_endpoint=self.api_endpoint, api_token=self.api_token)
        json_output = json.loads(argo.request())
        if json_output['items'] is not None:
            print("\nArgoCD applications:")
            for i in range(len(json_output['items'])):
                print(
                    "* %s" %
                    json.dumps(
                        json_output['items'][i]['metadata']['name'],
                        indent=4).strip('"'))
        else:
            logging.info("No applications found")

    def create_application(self, json_file: str):
        """ Create an application """
        data = fn.open_json_file(json_file)
        try:
            self.request(method="POST", data=data)
            logging.info(
                f"Successfully created application {data['metadata']['name']}")
        except BaseException:
            logging.error("Failed to create application")
            exit()

    def update_application(self, json_file: str):
        """ Send an Update request to update the applciation configuration """
        with open(json_file, 'r') as f:
            data = fn.open_json_file(json_file)
        try:
            self.request(
                method="PUT",
                data=data,
                uri=f"{data['metadata']['name']}")
            logging.info(
                f"Successfully updated application {data['metadata']['name']}")
        except BaseException:
            logging.error("Failed to update application")
            exit()

    def delete_application(self, method="DELETE", application_name=None):
        """ Send a Delete request to delete an application """
        try:
            self.request(method=method, uri=f"api/v1/applications/{application_name}")
            logging.info("Successfully deleted application")
        except BaseException:
            logging.error("Failed to delete application")
            exit()

    def list_repositories(self):
        """ Lists all repositories """
        table = PrettyTable()
        try:
            request = self.request(method="GET", uri="/api/v1/repositories")
            logging.info(
                f"Finished retrieving repositories")
        except BaseException:
            logging.error("Failed to retrieve repositories")
            exit()
        argo_repos = json.loads(str(request))
        for obj in argo_repos['items']:
            table.field_names = ['Repository', 'State', 'Type']
            row = [
                obj['repo'],
                obj['connectionState']['status'],
                obj['type']]
            table.add_row(row)
        print(table)