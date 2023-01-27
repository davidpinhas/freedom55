import requests
from prettytable import PrettyTable
from utils.fd55_config import Config
from utils.functions import Functions as fn
from utils.k8s import K8s
import json
import logging
logger = logging.getLogger()
config = Config()


class ArgoCD:
    def __init__(self, api_endpoint, api_token):
        self.api_endpoint = api_endpoint
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def load_response_json(self, response):
        json_output = response.json()
        logging.debug(f"Loaded response json:\n{json_output}")
        return json_output

    def get_applications(self):
        """ Get all ArgoCD applications """
        logging.info("Retrieving ArgoCD applications")
        argo = ArgoCD(api_endpoint=self.api_endpoint, api_token=self.api_token)
        table = PrettyTable()
        try:
            response = requests.request(
                headers=argo.headers,
                method="GET",
                url=f"{self.api_endpoint}/api/v1/applications")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            response_data = json.loads(response.text)
            for obj in range(len(response_data["items"])):
                response_obj = response_data['items'][obj]
                table.field_names = ['Application']
                row = [response_obj['metadata']['name']]
                table.add_row(row)
            print(f"\n{table}")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error listing ArgoCD applications:\n{response.text}')

    def create_application(self, json_file: str):
        """ Create an application """
        data = fn.open_json_file(json_file)
        try:
            response = fn.send_request(
                self,
                method="POST",
                data=data,
                headers=self.headers,
                base_url=self.api_endpoint,
                endpoint=f"/api/v1/applications")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            logging.info(
                f"Successfully created application {data['metadata']['name']}")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error creating ArgoCD application:\n{response.text}')

    def update_application(self, json_file: str):
        """ Send an Update request to update the applciation configuration """
        with open(json_file, 'r') as f:
            data = fn.open_json_file(json_file)
        try:
            response = fn.send_request(
                self,
                method="PUT",
                data=data,
                headers=self.headers,
                base_url=self.api_endpoint,
                endpoint=f"/api/v1/applications/{data['metadata']['name']}")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            logging.info(
                f"Successfully updated application {data['metadata']['name']}")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error updating ArgoCD application:\n{response.text}')

    def delete_application(self, application_name=None):
        """ Send a Delete request to delete an application """
        try:
            response = fn.send_request(
                self,
                method="DELETE",
                headers=self.headers,
                base_url=self.api_endpoint,
                endpoint=f"/api/v1/applications/{application_name}")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            logging.info("Successfully deleted application")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error deleting ArgoCD application:\n{response.text}')

    def list_repositories(self):
        """ List all repositories """
        table = PrettyTable()
        try:
            response = fn.send_request(
                self,
                method="GET",
                headers=self.headers,
                base_url=self.api_endpoint,
                endpoint=f"/api/v1/repositories")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            logging.info(
                f"Finished retrieving repositories")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error listing ArgoCD repositories:\n{response.text}')
        argo_repos = json.loads(str(response.text))
        for obj in argo_repos['items']:
            logging.debug(f"Repository data:\n{obj}")
            table.field_names = ['Repository', 'State', 'Type']
            row = [
                obj['repo'],
                obj['connectionState']['status'],
                obj['type']]
            table.add_row(row)
        print(table)

    def add_repo(self, repo_url, username=None, password=None, name=None):
        """ Adding a repository """
        if not name:
            name = repo_url.split("/")[-1].replace(".git", "")
        if not username or not password:
            payload = f'{{"repo": "{repo_url}","name": "{name}"}}'
        else:
            payload = f'{{"password": "{password}","repo": "{repo_url}","username": "{username}","name": "{name}"}}'
        json_output = json.loads(payload)
        indented_json_string = json.dumps(json_output, indent=4)
        logging.debug(f"Created payload:\n{indented_json_string}")
        try:
            response = fn.send_request(
                self,
                method="POST",
                headers=self.headers,
                data=json_output,
                base_url=self.api_endpoint,
                endpoint=f"/api/v1/repositories")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            logging.info(
                f"Created repository - {repo_url}")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error adding ArgoCD repository:\n{response.text}')

    def update_repo(self, repo_url, username=None, password=None, name=None):
        """ Update a repository """
        if not name:
            name = repo_url.split("/")[-1].replace(".git", "")
        if not username or not password:
            payload = f'{{"repo": "{repo_url}","name": "{name}"}}'
        payload = f'{{"password": "{password}","repo": "{repo_url}","username": "{username}","name": "{name}"}}'
        json_output = json.loads(payload)
        indented_json_string = json.dumps(json_output, indent=4)
        logging.debug(f"Created payload:\n{indented_json_string}")
        encoded_repo_url = str(repo_url).replace(
            '://', '%3A%2F%2F').replace('/', '%2F')
        try:
            response = fn.send_request(
                self,
                method="PUT",
                headers=self.headers,
                data=json_output,
                base_url=self.api_endpoint,
                endpoint=f"/api/v1/repositories/{encoded_repo_url}")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            logging.info(
                f"Updated repository - {repo_url}")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error updating ArgoCD repository:\n{response.text}')

    def delete_repo(self, repo_url=None):
        """ Delete a repository """
        encoded_repo_url = str(repo_url).replace(
            '://', '%3A%2F%2F').replace('/', '%2F')
        try:
            response = fn.send_request(
                self,
                method="DELETE",
                headers=self.headers,
                base_url=self.api_endpoint,
                endpoint=f"/api/v1/repositories/{encoded_repo_url}")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            logging.info(
                f"Deleted repository - {repo_url}")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error deleting ArgoCD repository:\n{response.text}')

    def export_argocd_settings(self):
        """ Export ArgoCD server settings """
        try:
            k8s_client = K8s(namespace="argocd")
            logging.info("Export started")
            kubectl_output = k8s_client.kubectl.run(
                [
                    "exec",
                    "-it",
                    f"{k8s_client.get_argocd_server_pod()}",
                    "-n",
                    "argocd",
                    "--",
                    "argocd",
                    "admin",
                    "export",
                    "-n",
                    "argocd"])
            clean_kubectl_output = kubectl_output.stdout.strip()
            print(clean_kubectl_output)
        except Exception as e:
            logging.error(
                f"An error occurred while exporting ArgoCD server settings: {e}")

    def import_argocd_settings(self, file):
        """ Import ArgoCD server settings """
        try:
            k8s_client = K8s(namespace="argocd")
            logging.info("Import started")
            k8s_client.copy_file_to_argocd_server_pod(file=file)
            k8s_client.kubectl.run(['exec',
                                    f'{k8s_client.get_argocd_server_pod()}',
                                    '-n',
                                    'argocd',
                                    '--',
                                    'argocd',
                                    'admin',
                                    'import',
                                    f'/tmp/{file}',
                                    '-n',
                                    'argocd'])
            logging.info("Import finished")
        except Exception as e:
            logging.error(
                f"An error occurred while importing ArgoCD server settings: {e}")
