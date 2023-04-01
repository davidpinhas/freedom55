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

    def get_tasks(self, task_type):
        self.refresh_config()
        response = requests.get(
            f"{self.url}/service/rest/v1/tasks",
            headers=self.headers,
            auth=self.auth)
        backup_task_id = json.loads(response.text)
        if task_type:
            for i in backup_task_id['items']:
                if i['type'] != f'{task_type}':
                    pass
                else:
                    logging.info(f"Backup task ID - '{i['id']}'")
                    return i['id']

    def get_backup_task(self):
        logging.info("Retrieving backup task ID")
        return self.get_tasks(task_type="db.backup")

    def get_repair_db_task(self):
        logging.info("Retrieving repair DB task ID")
        return self.get_tasks(task_type="blobstore.rebuildComponentDB")

    def get_repair_db_date_md_task(self):
        logging.info("Retrieving repair DB date metadata task ID")
        return self.get_tasks(task_type="rebuild.asset.uploadMetadata")

    def check_task_status(self, task_id, retries=10):
        task_status = False
        while task_status != 'WAITING':
            for i in range(retries):
                task_status = self.check_task_state(task_id)
                if task_status == 'WAITING':
                    logging.info("Finished backup task")
                    break
                time.sleep(2)

    def run_task(self, task_id=None):
        if task_id:
            self.refresh_config()
            response = requests.post(
                url=f'{self.url}/service/rest/v1/tasks/{task_id}/run',
                headers=self.headers,
                auth=self.auth)
            self.check_task_status(task_id=task_id)
            if response.status_code not in range(200, 207):
                logging.error(
                    f"Backup task failed with status code {response.status_code}")
                exit(1)

    def run_backup_task(self):
        task_id = self.get_backup_task()
        logging.info("Running backup task")
        self.run_task(task_id=task_id)

    def run_repair_db_task(self):
        task_id = self.get_repair_db_task()
        logging.info("Running repair DB task")
        self.run_task(task_id=task_id)

    def run_repair_db_date_md(self):
        task_id = self.get_repair_db_date_md_task()
        logging.info("Running repair DB date metadata task")
        self.run_task(task_id=task_id)

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
