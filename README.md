# Freedom 55
Freedom 55 CLI is an operational tool written in Python by David Pinhas to maintain, modify and operate a homelab.

```bash
$ fd55
Usage: fd55 [OPTIONS] COMMAND [ARGS]...

  Freedom 55 CLI tools.

  The freedom 55 CLI is an operational tool crafted by David Pinhas To
  maintain, modify and operate a homelab.

Options:
  --log TEXT  Logging level (INFO, WARNING, ERROR, CRITICAL, DEBUG)
  --help      Show this message and exit.

Commands:
  argo  ArgoCD commands
  oci   OCI commands
  sops  SOPS with Age encryption commands
  tf    Terraform commands
```

## Requirements
- Python 3.10 or higher
- Click - can be installed using `$ pip install click`
- OCI - can be installed using `$ pip install oci oci-cli`
- OCI config file - The config file (usually located under the ~/.oci/config directory) is required to have the [minimum required keys and OCIDs](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#Required_Keys_and_OCIDs).

Follow [Oracle documentation](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#configfile) to configure the OCI. 

## Installation
In order to install the CLI on your local machine, you can clone the repository and utilize the startup.sh script:
```bash
git clone https://github.com/davidpinhas/fd55.git
cd fd55
bash startup.sh
```
The script will create a virtual environment and provide steps to configure the alias for sourcing the venv.

## Usage
To use the Freedom 55 CLI, we'll first call fd55, than the component and it's sub-command:
```bash
$ fd55 [COMPONENT] [COMMAND] [OPTIONS]
```
For example:
```bash
$ fd55 oci encrypt --string "Random text"
```

### Options
- `--log DEBUG`: (Optional) Specify the log level. If not provided, the default level is INFO.
- `--help`: (Optional) Show the help message and exit.

## Components
Freedom 55 lets you integrate a variaty of tools and utilize them through one multi-tool.
The vision is to provide you the freedom to work with multiple tools without installing any prequisites.

Here's a list of currently supported tools (currently limited support):
* [ArgoCD](###Argocd)
* [OCI](###OCI)
* [SOPS](###SOPS)
* [Terraform](###Terraform)

### ArgoCD
The ArgoCD component will be able to retrieve app info along with managing the ArgoCD server and its applications.

Get all ArgoCD applications:
```bash
$ fd55 argo get-apps
```

Create an application:
```bash
$ fd55 argo create-app -f application-yaml
```

### OCI
OCI (Oracle Cloud Infrastructure) component utilizes the KMS feature and lets you encrypt and decrypt a string.

To encrypt a secret, you can provide it as a string:
```bash
$ fd55 oci encrypt --string "This is my secret"
```

Expected output:
```
INFO:root:Validating OCI config file
INFO:root:All config keys exist
INFO:root:Encrypting string with KMS
INFO:root:Encrypted string value - Qf7eN7k3cJBlAFpAtSVaPqM.... (KMS encrypted secret)
```

For decrypting a secret, the KMS encrypted value needs to be provided as a string (decrpyting needs to be performed with the same key the value was encrypted to begin with):
```bash
$ fd55 oci decrypt --string Qf7eN7k3cJBlAFpAtSVaPqM....
```

Expected output:
```
INFO:root:Validating OCI config file
INFO:root:All config keys exist
INFO:root:Decrypting string with KMS
INFO:root:Decrypted string - This is my secret
```

### SOPS
You can use the SOPS component to encrypt and decrypt files using Age encryption.
Both encrypt and decrypt operations require an input and output file arguments.

For example, we can encrypt a file using SOPS with the following command:
```bash
fd55 sops encrypt --input_file test.yaml --output_file test.yaml2
```

For encrypting specific values, you may use the ``--encrypted_regex`` or ``-r`` flags to set a regex condition to encrypt:
```bash
fd55 sops encrypt --input_file test.yaml --output_file test.yaml2 -r ingress
```

To encrypt multiple values, use the ``|`` sign:
```bash
fd55 sops encrypt --input_file test.yaml --output_file test.yaml2 -r ingress|domain|spec
```

In order to decrypt a file, use the following:
```bash
fd55 sops decrypt --input_file test.yaml --output_file test.yaml2
```

### Terraform
To run the Terraform commands, you will need to provide the path of Terraform project with ``--path`` or ``-p`` flags.

For example, run the command below to get the output of the Terraform plan:
```bash
fd55 tf output -p /Users/davidpinhas/workspace/cloud/k3s-oci-cluster/example
```

## License
This project is licensed under the MIT License. See [LICENSE](/LICENSE.md) for more details.
