import logging
import subprocess
from kubernetes import client, config


class Kubectl:
    def __init__(self):
        self.command = "kubectl"

    def run(self, args, shell=None):
        try:
            if shell:
                args = self.command + args
                proc = subprocess.run(
                    args,
                    shell=True,
                    capture_output=True,
                    text=True,
                    universal_newlines=True)
                lines = proc.stdout.split("\n")
                for line in lines:
                    if line:
                        logging.info(line)
            else:
                args = [self.command] + args
                proc = subprocess.run(args, capture_output=True, text=True)
            return proc
        except subprocess.CalledProcessError as e:
            logging.error(f'Error: {e}')
            logging.error(f'Command: {e.cmd}')
            logging.error(f'Return code: {e.returncode}')
            logging.error(f'Output: {e.output}')


class K8s:
    def __init__(self, resource_type=None, namespace=None):
        self.resource_type = resource_type
        self.namespace = namespace
        self.kubectl = Kubectl()
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def get_argocd_server_pod(self):
        """ Get ArgoCD server pod name """
        proc = K8s().v1.list_namespaced_pod(namespace=self.namespace)
        for item in proc.items:
            if str(item.metadata.name).startswith("argocd-server"):
                return item.metadata.name

    def copy_file_to_argocd_server_pod(self, file):
        try:
            logging.info("Copying file to ArgoCD server pod")
            K8s().kubectl.run(["cp",
                               f"{file}",
                               f"{self.get_argocd_server_pod()}:/tmp/",
                               "-n",
                               f"{self.namespace}"])
        except Exception as e:
            logging.error(f"An error occurred: {e}")
