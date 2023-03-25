import subprocess
import os
import json
import datetime
import logging
import requests
from tabulate import tabulate
from fd55.utils.fd55_config import Config
config = Config()


class NexusRepositoryManager:
    def __init__(self):
        self.url = f"{str(config.get('NEXUS', 'url'))}"
        self.nexus_pod = self.get_nexus_pod()
        self.backup_dir = f"nexus_data_{datetime.datetime.now().strftime('%y%m%d_%H%M%S')}"
        self.headers = {'Accept': 'application/json'}
        self.auth = (f"{str(config.get('NEXUS', 'user'))}", f"{str(config.get('NEXUS', 'password'))}")

    def get_nexus_pod(self):
        nexus_pods = subprocess.check_output(
            [
                'kubectl',
                'get',
                'pods',
                '-n',
                'nexus',
                '-o',
                'jsonpath="{.items[*].metadata.name}"']).decode('utf-8').strip('"\n').split(' ')
        if not nexus_pods:
            logging.warning('No nexus pods found')
            exit(1)
        return nexus_pods[0]

    def check_backup_directory(self):
        logging.info(f"Checking for backup dir in pod '{self.nexus_pod}'")
        check_dir_exists_command = f'kubectl exec -n nexus {self.nexus_pod} -- test -d /nexus-data/backup'
        if subprocess.call(check_dir_exists_command, shell=True) != 0:
            logging.error('Directory /nexus-data/backup not found in the pod')
            exit(1)

        check_dir_empty_command = f'kubectl exec -n nexus {self.nexus_pod} -- test -d /nexus-data/backup'
        if subprocess.call(check_dir_empty_command, shell=True) != 0:
            logging.warning(
                f'Directory /nexus-data/backup is empty in {self.nexus_pod}')
            exit(1)

    def get_backup_task(self):
        logging.info("Retrieving backup task ID")
        response = requests.get(f"{self.url}/service/rest/v1/tasks", headers=self.headers, auth=self.auth)
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

    def copy_backup_directory(self):
        logging.info("Copying backup directory to local machine")
        if not os.path.exists('nexus-conf-backup'):
            os.mkdir('nexus-conf-backup')
        os.mkdir(f"nexus-conf-backup/{self.backup_dir}")
        cmd = f"kubectl -n nexus cp nexus/{self.nexus_pod}:/nexus-data nexus-conf-backup/{self.backup_dir}"
        subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def print_directory_contents(self, new_dir=False):
        if new_dir == True:
            backup_dir_content = f"nexus-conf-backup/{self.backup_dir}/backup"
            logging.info(f"Searching files in dir '{self.backup_dir}'")
        else:
            snapshot_dirs = [dir_name for dir_name in os.listdir('nexus-conf-backup/') if dir_name.startswith('nexus_data_')]
            snapshot_dirs.sort(reverse=True)
            latest_snapshot_dir = snapshot_dirs[0]
            backup_dir_content = f"nexus-conf-backup/{latest_snapshot_dir}/backup"
            logging.info(f"Searching files in dir {latest_snapshot_dir}")
        files = os.listdir(backup_dir_content)
        config_files = []
        security_files = []
        component_files = []
        for f in files:
            if 'config-' in f:
                config_files.append(f)
            elif 'security-' in f:
                security_files.append(f)
            elif 'component-' in f:
                component_files.append(f)
        config_files = sorted(config_files)
        security_files = sorted(security_files)
        component_files = sorted(component_files)
        config_table = [[i + 1, f] for i, f in enumerate(config_files)]
        security_table = [[i + 1, f] for i, f in enumerate(security_files)]
        component_table = [[i + 1, f] for i, f in enumerate(component_files)]
        logging.info(f"Contents of backup")
        print("-------------------------")
        print(tabulate(config_table, headers=["#", "Config Backup Files"]))
        print("-------------------------")
        print(tabulate(security_table, headers=["#", "Security Backup Files"]))
        print("-------------------------")
        print(
            tabulate(
                component_table,
                headers=[
                    "#",
                    "Component Backup Files"]))