import requests

class ArgoCD:
    def __init__(self, api_endpoint, api_token):
        self.api_endpoint = api_endpoint
        self.api_token = api_token

    def get_applications(self):
        """ Get all ArgoCD applications """
        url = f"{self.api_endpoint}/api/v1/applications"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(url, headers=headers)
        print(response)
        if response.status_code != 200:
            raise Exception(f"Failed to get applications: {response.json()['message']}")
        return response.json()["items"]

    def create_application(self, application_name, repository_url):
        """ Create an application """
        url = f"{self.api_endpoint}/api/v1/applications"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        data = {"metadata": {"name": application_name}, "spec": {"repoURL": repository_url}}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise Exception(f"Failed to create application: {response.json()['message']}")

    def update_application(self, application_name, repository_url):
        """ Send an Update request to update the applciation configuration """
        url = f"{self.api_endpoint}/api/v1/applications/{application_name}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        data = {"spec": {"repoURL": repository_url}}
        response = requests.put(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to update application: {response.json()['message']}")

    def delete_application(self, application_name):
        """ Send a Delete request to delete an application """
        url = f"{self.api_endpoint}/api/v1/applications/{application_name}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.delete(url, headers=headers)
        
        # Check the response status code
        if response.status_code != 200:
            raise Exception(f"Failed to delete application: {response.json()['message']}")
