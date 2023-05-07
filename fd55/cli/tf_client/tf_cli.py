import subprocess
import logging
from fd55.utils.functions import Functions as fn
logger = logging.getLogger()


class TerraformCli:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def tf_init(self):
        """ Run Terraform init """
        cmd = ["terraform", "init"]
        logging.info(
            f"Initializing Terraform in directory {self.working_dir}")
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True)
            fn.log_process_output(proc)
            proc.communicate()
            if proc.returncode != 0:
                logging.error(
                    f"Terraform init failed with exit code {proc.returncode}")
            return proc.returncode
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode

    def tf_plan(self, outfile=None):
        """ Run Terraform plan """
        cmd = ["terraform", "plan"]
        if outfile:
            cmd.extend(["-out", outfile])
        logging.info(f"Running Terraform plan")
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True)
            fn.log_process_output(proc)
            proc.communicate()
            if proc.returncode != 0:
                logging.error(
                    f"Terraform plan failed with exit code {proc.returncode}")
            return proc.returncode
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode

    def tf_apply(self, planfile):
        """ Run Terraform apply """
        cmd = ["terraform", "apply", planfile]
        logging.info(f"Applying Terraform changes")
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True)
            fn.log_process_output(proc)
            proc.communicate()
            if proc.returncode != 0:
                logging.error(
                    f"Terraform apply failed with exit code {proc.returncode}")
            return proc.returncode
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode

    def tf_destroy(self):
        """ Run Terraform destroy """
        cmd = ["terraform", "destroy", "-auto-approve"]
        logging.info(f"Destroying Terraform infrastructure")
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True)
            fn.log_process_output(proc)
            proc.communicate()
            if proc.returncode != 0:
                logging.error(
                    f"Terraform destroy failed with exit code {proc.returncode}")
            return proc.returncode
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode

    def tf_output(self, output_name):
        """ Get the output of a Terraform variable """
        cmd = ["terraform", "output", output_name]
        logging.info(f"Retrieving Terraform output '{output_name}'")
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True)
            fn.log_process_output(proc)
            output, _ = proc.communicate()
            if proc.returncode != 0:
                logging.error(
                    f"Failed to retrieve Terraform output '{output_name}'")
                return None
            else:
                return output.strip()
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return None
