import subprocess
import logging

logger = logging.getLogger()


class TerraformCli:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.logger = logging.getLogger(__name__)

    def tf_init(self):
        cmd = ["terraform", "init"]
        self.logger.info(
            f"Initializing Terraform in directory {self.working_dir}")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            self.logger.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            self.logger.error(e.stderr)
            return e.returncode

    def tf_plan(self, outfile=None):
        cmd = ["terraform", "plan"]
        if outfile:
            cmd.extend(["-out", outfile])
        self.logger.info(f"Running Terraform plan")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            self.logger.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            self.logger.error(e.stderr)
            return e.returncode

    def tf_apply(self, planfile):
        cmd = ["terraform", "apply", planfile]
        self.logger.info(f"Applying Terraform changes")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            self.logger.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            self.logger.error(e.stderr)
            return e.returncode

    def tf_destroy(self):
        cmd = ["terraform", "destroy", "-auto-approve"]
        self.logger.info(f"Destroying Terraform resources")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.working_dir,
                check=True,
                capture_output=True,
                text=True)
            self.logger.debug(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            self.logger.error(e.stderr)
            return e.returncode
