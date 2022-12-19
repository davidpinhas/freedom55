from python_terraform import *
import logging

logger = logging.getLogger()

class TerraformCli:

    def tf_path(path):
        tf = Terraform(working_dir=path)
        return tf

    def tf_init(path):
        logging.info(TerraformCli.tf_path(path).init(no_color=IsFlagged, refresh=False, capture_output=True)[1])

    def tf_plan(path):
        logging.info(TerraformCli.tf_path(path).plan(no_color=IsFlagged, refresh=False, capture_output=True)[1])

    def tf_apply(path):
        approve = {"auto-approve": True}
        logging.info(TerraformCli.tf_path(path).apply(**approve)[1])

    def tf_output(path):
        logging.info(TerraformCli.tf_path(path).output_cmd()[1])

    def tf_destroy(path):
        logging.info(TerraformCli.tf_path(path).destroy()[1])