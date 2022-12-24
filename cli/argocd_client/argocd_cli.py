import requests
from utils.fd55_config import Config

config = Config()


class ArgoCD:
    def __init__(self, api_endpoint, api_token):
        self.api_endpoint = api_endpoint
        self.api_token = api_token


    def request(self, uri=None, method="GET", data=None):
        if uri is not None:
            url = f"{self.api_endpoint}/api/v1/applications/{uri}"
        else:
            url = f"{self.api_endpoint}/api/v1/applications"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        if data is not None:
            data = data
            response = requests.request(
                url, method=method, headers=headers, json=data)
        else:
            response = requests.request(url=url, method=method, headers=headers)
        print(response)
        if response.status_code != 200:
            raise Exception(f"Failed to execute: {response.json()['message']}")
        return response.json()["items"]

    def get_applications(self):
        """ Get all ArgoCD applications """
        argo = ArgoCD(api_endpoint=f"{config.get('ARGOCD', 'url')}", api_token=f"test")
        argo.request()

    def create_application(self, application_name, repository_url):
        """ Create an application """
        ArgoCD.request(method="post", data={"metadata": {
                       "name": application_name}, "spec": {"repoURL": repository_url}})

    def update_application(self, application_name, repository_url):
        """ Send an Update request to update the applciation configuration """
        ArgoCD.request(method="put", uri={application_name}, data={
                       "spec": {"repoURL": repository_url}})

    def delete_application(self, application_name):
        """ Send a Delete request to delete an application """
        ArgoCD.request(method="delete", uri={application_name})
