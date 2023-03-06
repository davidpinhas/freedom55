import subprocess
import logging

logger = logging.getLogger()


class TerraformCli:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def tf_init(self):
        cmd = ["terraform", "init"]
        logging.info(
            f"Initializing Terraform in directory {self.working_dir}")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            logging.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode


    def tf_plan(self, outfile=None):
        cmd = ["terraform", "plan"]
        if outfile:
            cmd.extend(["-out", outfile])
        logging.info(f"Running Terraform plan")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            logging.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode

    def tf_apply(self, planfile):
        cmd = ["terraform", "apply", planfile]
        logging.info(f"Applying Terraform changes")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            logging.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode

    def tf_output(self):
        cmd = ["terraform", "output"]
        logging.info(f"Running Terraform output")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            logging.info(f"Terraform output result:\n{result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode

    def tf_destroy(self):
        cmd = ["terraform", "destroy", "-auto-approve"]
        logging.info(f"Destroying Terraform resources")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            logging.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)
            return e.returncode
