import requests
import yaml
import os
from os import listdir
from os.path import isfile, join
import datetime
from InquirerPy import inquirer
from prettytable import PrettyTable
from fd55.utils.fd55_config import Config
from fd55.utils.functions import Functions as fn
from fd55.utils.k8s import K8s
import json
import logging
logger = logging.getLogger()
config = Config()


class ArgoCD:
    def __init__(self, api_endpoint=None, api_token=None):
        self.config_dir = config.get_config_dir()
        self.api_endpoint = api_endpoint
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if not api_token:
            self.headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        if not os.path.exists(f'{self.config_dir}/argocd'):
            os.mkdir(f'{self.config_dir}/argocd')

    def load_response_json(self, response):
        """ Load response as JSON """
        json_output = response.json()
        logging.debug(f"Loaded response json:\n{json_output}")
        return json_output

    def check_exports_dir(self):
        if not os.path.exists(f'{self.config_dir}/argocd/exports'):
            os.mkdir(f'{self.config_dir}/argocd/exports')

    def select_export_file(self):
        """ Prompt the user to select ArgoCD export file """
        try:
            exports_dir = join(self.config_dir, 'argocd', 'exports')
            logging.info(
                f"Searching for export files in direcrory '{exports_dir}'")
            files = [
                f for f in listdir(exports_dir) if isfile(
                    join(
                        exports_dir,
                        f))]
            if not files:
                raise ValueError("No export files found in directory.")
            selected_export = inquirer.select(
                message='Select an export file:',
                choices=files).execute()
            selected_export_file = join(exports_dir, selected_export)
            logging.info(f"Using export file: '{selected_export_file}'")
            return selected_export
        except OSError:
            logging.error(
                f"Failed to access export files directory '{exports_dir}'.")
            return None
        except ValueError as ve:
            logging.error(str(ve))
            return None

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

    def create_application(self, file: str = None):
        """ Create an application """
        if file is None:
            raise ValueError(
                'At least one of json_file or yaml_file must be provided')
        file_format = fn.validate_data_type(file)
        if file_format == 'json':
            data = fn.open_json_file(file)
        elif file_format == 'yaml':
            with open(file, 'r') as f:
                yaml_data = f.read()
            json_data = yaml.safe_load(yaml_data)
            with open('temp.json', 'w') as f:
                json.dump(json_data, f)
            with open('temp.json', 'r') as f:
                data = json.load(f)
            os.remove('temp.json')
        else:
            raise ValueError(f'Invalid file format: {file_format}')
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
            r = json.loads(response.text)
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f"Encountered error creating ArgoCD application: {r['error']}")

    def update_application(self, json_file: str):
        """ Update applciation configuration """
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
        """ Delete an application """
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
        """ Add repository """
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
            self.check_exports_dir()
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
            file_name = f"argocd-export-{datetime.datetime.now().strftime('%d-%m-%Y')}.yaml"
            with open(f'{self.config_dir}/argocd/exports/{file_name}', 'w') as file:
                file.write(clean_kubectl_output)
                logging.info(
                    f"saved ArgoCD export to file: {self.config_dir}/argocd/exports/{file_name}")
        except Exception as e:
            logging.error(
                f"An error occurred while exporting ArgoCD server settings: {e}")

    def import_argocd_settings(self):
        """ Import ArgoCD server settings """
        try:
            k8s_client = K8s(namespace="argocd")
            logging.info("Import started")
            export_file = self.select_export_file()
            k8s_client.copy_file_to_argocd_server_pod(
                file=f"{self.config_dir}/argocd/exports/{export_file}")
            k8s_client.kubectl.run(['exec',
                                    f'{k8s_client.get_argocd_server_pod()}',
                                    '-n',
                                    'argocd',
                                    '--',
                                    'argocd',
                                    'admin',
                                    'import',
                                    f'/tmp/{export_file}',
                                    '-n',
                                    'argocd'])
            logging.info("Import finished")
        except Exception as e:
            logging.error(
                f"An error occurred while importing ArgoCD server settings: {e}")

    def create_jwt(self, username, password):
        """ Create ArgoCD JWT token """
        logging.info("Generating JWT token")
        argo = ArgoCD(api_endpoint=self.api_endpoint, api_token=self.api_token)
        try:
            payload = f'{{"username":"{username}","password":"{password}"}}'
            response = requests.request(
                headers=argo.headers,
                method="POST",
                data=payload,
                url=f"{self.api_endpoint}/api/v1/session")
            if response.status_code != 200:
                raise requests.exceptions.HTTPError
            response_data = json.loads(response.text)
            logging.info(f"Created JWT Token: {response_data['token']}")
        except requests.exceptions.HTTPError:
            logging.error(f'Failed with status code: {response.status_code}')
            logging.error(
                f'Encountered error creating JWT:\n{response.text}')
