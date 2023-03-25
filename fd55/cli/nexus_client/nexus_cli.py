import json
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

    def get_backup_task(self):
        logging.info("Retrieving backup task ID")
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

    def run_backup_task(self):
        task_id = self.get_backup_task()
        logging.info("Running backup task")
        response = requests.post(
            url=f'{self.url}/service/rest/v1/tasks/{task_id}/run',
            headers=self.headers,
            auth=self.auth)
        if response.status_code not in range(200, 207):
            logging.error(
                f"Backup task failed with status code {response.status_code}")
            exit(1)

    def list_repositories(self):
        logging.info("Retrieving list of repositories")
        response = requests.get(
            f"{self.url}/service/rest/v1/repositories",
            headers=self.headers,
            auth=self.auth)
        repositories = json.loads(response.text)
        logging.info("List of repositories:")
        print(f"{json.dumps(repositories, indent=4)}")
        return repositories

    def list_blob_stores(self):
        logging.info("Retrieving list of blob stores")
        response = requests.get(
            f"{self.url}/service/rest/v1/blobstores",
            headers=self.headers,
            auth=self.auth)
        blob_stores = json.loads(response.text)
        logging.info("List of blob stores:")
        print(f"{json.dumps(blob_stores, indent=4)}")
        return blob_stores
