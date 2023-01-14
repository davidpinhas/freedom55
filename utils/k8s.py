import subprocess
from kubernetes import client, config


class Kubectl:
    def __init__(self):
        self.command = "kubectl"

    def run(self, args):
        args = [self.command] + args
        return subprocess.run(args, capture_output=True, text=True)


class K8s:
    def __init__(self, resource_type=None, namespace=None):
        self.resource_type = resource_type
        self.namespace = namespace
        self.kubectl = Kubectl()
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def get_argocd_server_pod(self):
        """ Get ArgoCD server pod name """
        ret = K8s().v1.list_namespaced_pod(namespace=self.namespace)
        for item in ret.items:
            if str(item.metadata.name).startswith("argocd-server"):
                return item.metadata.name
