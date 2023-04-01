import json
import time
import logging
import requests
from fd55.utils.fd55_config import Config
config = Config()


class NexusRepositoryManager:
    def __init__(self):
        self.url = f"{str(config.get('NEXUS', 'url'))}"
        self.headers = {'Accept': 'application/json'}
        self.auth = (
            f"{str(config.get('NEXUS', 'user'))}",
            f"{str(config.get('NEXUS', 'password'))}")

    def refresh_config(self):
        config = Config()
        self.auth = (
            f"{str(config.get('NEXUS', 'user'))}",
            f"{str(config.get('NEXUS', 'password'))}")

    def check_task_state(self, id):
        self.refresh_config()
        response = requests.get(
            f"{self.url}/service/rest/v1/tasks/{id}",
            headers=self.headers,
            auth=self.auth)
        logging.info(
            f"Task state: '{json.loads(response.text)['currentState']}'")
        return json.loads(response.text)['currentState']

    def get_backup_task(self):
        logging.info("Retrieving backup task ID")
        self.refresh_config()
        response = requests.get(
            f"{self.url}/service/rest/v1/tasks",
            headers=self.headers,
            auth=self.auth)
        backup_task_id = json.loads(response.text)
        for i in backup_task_id['items']:
            if i['type'] != 'db.backup':
                pass
            else:
                logging.info(f"Backup task ID - '{i['id']}'")
                return i['id']

    def run_backup_task(self, retries=10):
        task_status = False
        task_id = self.get_backup_task()
        logging.info("Running backup task")
        self.refresh_config()
        response = requests.post(
            url=f'{self.url}/service/rest/v1/tasks/{task_id}/run',
            headers=self.headers,
            auth=self.auth)
        while task_status != 'WAITING':
            for i in range(retries):
                task_status = self.check_task_state(task_id)
                if task_status == 'WAITING':
                    logging.info("Finished backup task")
                    break
                time.sleep(2)

        if response.status_code not in range(200, 207):
            logging.error(
                f"Backup task failed with status code {response.status_code}")
            exit(1)

    def list_repositories(self, print_list=True):
        logging.info("Retrieving list of repositories")
        self.refresh_config()
        try:
            response = requests.get(
                f"{self.url}/service/rest/v1/repositories",
                headers=self.headers,
                auth=self.auth)
            response.raise_for_status()  # raise an exception if status code indicates an error
        except requests.exceptions.HTTPError as e:
            logging.error(f"Failed to retrieve list of repositories: {e}")
            return None

        if print_list:
            logging.info("List of repositories:")
            print(f"{json.dumps(json.loads(response.text), indent=4)}")
        return json.loads(response.text)

    def list_blob_stores(self, print_list=True):
        logging.info("Retrieving list of blob stores")
        self.refresh_config()
        response = requests.get(
            f"{self.url}/service/rest/v1/blobstores",
            headers=self.headers,
            auth=self.auth)
        if print_list:
            logging.info("List of blob stores:")
            print(f"{json.dumps(json.loads(response.text), indent=4)}")
        return json.loads(response.text)
