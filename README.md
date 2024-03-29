![](images/Freedom55.png)
____

The operational client for maintaining, modifying, and operating your infrastructure.
Written in Python by David Pinhas, this multi-tool is constantly expanding to support more integrations. Make your homelab management a ***breeze*** with Freedom 55 CLI.

The goal of this project is to give you the freedom to work efficiently and effectively with one unified tool.

![](images/menu.gif)

## Menu

-   [Requirements](#Requirements)
-   [Installation](#Installation)
    -   [Installing Pip Binary](#Installing-Pip-Binary)
    -   [Windows Install](#Windows-Install)
-   [Usage](#Usage)
    -   [Options](#Options)
    -   [Configuration](#Configuration)
-   [Integrations](#Integrations)
    -   [ArgoCD](#ArgoCD)
    -   [OCI](#OCI)
    -   [SOPS](#SOPS)
    -   [Terraform](#Terraform)
    -   [Cloudflare](#Cloudflare)
    -   [ChatGPT](#ChatGPT)
-   [Contribution](#Contribution)
-   [License](#License)

## :warning: Disclaimer
- Not production ready! The tool is currently in Alpha version and is under active development. Therefore, it may contain bugs and incomplete features.<br>
- The versioning of the tool might reset in the future as the tool matures and approaches a stable release. <br>
Please use the tool at your own risk and report any issues or feedback.

## Requirements
- Python 3.10 or higher - Ensure `Python3.10`, `Pip3` and `Virtualenv` are installed
- Install Python dependencies - `$ pip3 install -r requirements.txt` [required for running tests locally]
- OCI keys and OCIDs - In order to [configure Freedom 55](#configuration) the OCI integration, you will need the [minimum required keys and OCIDs](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#Required_Keys_and_OCIDs)
- Freedom55 CLI requires the following clients to be locally installed:  
  Terraform CLI - https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli  
  OCI CLI - https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm  
  SOPS CLI - https://github.com/mozilla/sops#download  

## Installation
In order to install the CLI on your local machine, you can clone the repository and utilize the startup.sh script:
```bash
git clone https://github.com/davidpinhas/freedom55.git
cd freedom55
source startup.sh
```

The script will create a virtual environment and provide steps to configure the alias for sourcing the venv.

### Installing Pip Binary (Recommended)
To install the Freedom 55 CLI as a binary, you'll need to build the binary and install it using Pip3:
```bash
python3 -m build
pip3 install dist/fd55-$VERSION.tar.gz
```

Installing Freedom 55 as a binary is the recommended approach, as it provides improved performance when using the CLI, leading to faster execution times and a more efficient workflow.

### Windows Install
To source the startup.sh file, you can use [Git Bash](https://git-scm.com/downloads), which can simplify the installation process.<br>
Press the Windows Key > Search and press Git Bash > Follow the steps mentioned [above](#Installation).

For more details, read more on [What is Git Bash](https://www.gitkraken.com/blog/what-is-git-bash).

On Windows systems, the command "`fd55 config`" might result with the following error:
```bash
prompt_toolkit.output.win32.NoConsoleScreenBufferError: Found xterm, while expecting a Windows console. Maybe try to run this program using "winpty" or run it in cmd.exe instead. Or otherwise, in case of Cygwin, use the Python executable that is compiled for Cygwin.
```

To fix this issue, you'll need to use the **winpty** command to run the `fd55 config` command on Windows systems. This is because winpty is a compatibility layer that allows you to run console programs that are not natively supported on Windows.

By using winpty, you can run the `fd55 config` command without encountering any errors. Simply run the following command in your terminal:
```bash
winpty fd55 config start
```

## Usage
To use the Freedom 55 CLI, we'll first call fd55, than the integration and its command:
```bash
fd55 [INTEGRATION] [COMMAND] [OPTIONS] [FLAGS]
```

For example:
```bash
fd55 oci kms encrypt --string "Random text"
```

## Options
- `-v/--Verbose debug`: (Optional) Specify the log level. If not provided, the default level is 'info'.
- `--help`: (Optional) Show the help message and exit.

## Configuration
To configure Freedom 55 CLI with your desired integrations, run the `fd55 config start` command:
```bash
fd55 config start
2023-01-17 22:56:13,438|INFO|Running config validation
? Select integrations to configure
  ◉ OCI
  ◉ SOPS
  ○ ARGOCD
  ○ TERRAFORM
❯ ○ CLOUDFLARE
  ◉ AI
```

The `config start` command will guide you through the configuration process and request the required parameters for the selected integrations.

To configure a specific integration, you can run the `set` command with the integration:
```bash
fd55 config argo set [FLAGS]
```

for example, to set the ArgoCD Base URL and API token, run this command:
```bash
fd55 config argo set --url https://argo.domain.com --api-token $API_TOKEN
```

For more details, use the `fd55 config --help` or `fd55 config cf set --help` command to get a list of all available options.

In order to set a custom path for the config.ini file, you can set the `FD55_CONFIG_FILE_PATH` environment variable.
**Note** that this will treat the directory of the `config.ini` file as the **home directory** of the Freedom 55 CLI.  
This can be done by executing the following command in your terminal:
```bash
export FD55_CONFIG_FILE_PATH="path/to/config.ini"
```

Once this environment variable is set, the Freedom 55 CLI will use the custom path for the `config.ini` file when running commands.  
Please note that this step may vary depending on the operating system you are using and the way environment variables are set. If you wish to make this change permanent, You should add this line to your shell profile file such as .bash_profile or .bashrc.

## Integrations
Freedom 55 is a powerful multi-tool that simplifies your workflow by integrating a variety of tools into a single interface. <br>With Freedom 55, you can use a single tool instead of juggling multiple CLIs, which can clutter your environment and can be pretty overwhelming.

Here's a list of currently supported tools (limited support):
* [ArgoCD](#Argocd)
* [OCI](#OCI)
* [SOPS](#SOPS)
* [Terraform](#Terraform)
* [Cloudflare](#Cloudflare)
* [ChatGPT](#ChatGPT)

## ArgoCD
---
The [ArgoCD](https://argo-cd.readthedocs.io/en/stable/) integration allows you to retrieve application information and manage the ArgoCD server and its applications.

### Commands
- [Repo](#Repo)
- [App](#App)
- [Server](#Server)

This integration requires the following keys:
* `url` - ArgoCD endpoint, for example: https://argo.mydomain.com
* `api_token` - The API token with the required permission for managing applications. For generating a token [ArgoCD Docs](https://argo-cd.readthedocs.io/en/latest/user-guide/commands/argocd_account_generate-token/).

To modify an ArgoCD application, you will need to provide a [JSON](https://www.json.org/json-en.html) file with the desired application specifications.
Here's an example of a simple JSON file application spec:
```json
{
  "kind": "Application",
  "metadata": {
    "name": "my_app1",
    "namespace": "argocd"
  },
  "spec": {
    "destination": {
      "namespace": "my_app1",
      "server": "https://kubernetes.default.svc"
    },
    "project": "default",
    "source": {
      "path": "my_app1-chart",
      "repoURL": "https://github.com/$USER/my_app1.git",
      "targetRevision": "HEAD"
    },
    "syncPolicy": {
      "automated": {
        "prune": true,
        "selfHeal": true
      },
      "syncOptions": [
        "CreateNamespace=true"
      ]
    }
  }
}
```

For full details on the JSON payload, you can refer to the ArgoCD API Swagger documentation in the ArgoCD web interface. <br>To access it, navigate to your ArgoCD server in your web browser:
https://argo.mydomain.com/swagger-ui.

## Repo
### Get Repositories
Get all ArgoCD applications:
```bash
fd55 argo repo list
```

Expected output:
```
2023-01-13 07:31:52,957|INFO|Finished retrieving repositories
+---------------------------------------------------------+------------+------+
|                        Repository                       |   State    | Type |
+---------------------------------------------------------+------------+------+
|     https://github.com/davidpinhas/private-repo.git     | Successful | git  |
|      https://github.com/davidpinhas/public-repo.git     | Successful | git  |
+---------------------------------------------------------+------------+------+
```

### Create Repository
Swagger ref - https://argo.mydomain.com/swagger-ui#operation/RepositoryService_CreateRepository

To create an application, use the `-f` option to provide the json file application spec:
```bash
fd55 argo repo create -r https://github.com/davidpinhas/mc-server.git --username $USER --password $PASSWORD
```

Expected output:
```
2023-01-13 07:35:52,900|INFO|Created repository - https://github.com/davidpinhas/mc-server.git
```

### Update Repository
Swagger ref - https://argo.mydomain.com/swagger-ui#operation/RepositoryService_UpdateRepository

To update an application:
```bash
fd55 argo repo update --repo-url https://github.com/davidpinhas/mc-server.git --username $USER --password $PASSWORD
```

Expected output:
```
2023-01-13 07:38:05,468|INFO|Updated repository - https://github.com/davidpinhas/mc-server.git
```

### Delete Repository
Swagger ref - https://argo.mydomain.com/swagger-ui#operation/RepositoryService_DeleteRepository

To delete an application, use the `-n` option to provide the name of the application you wish to delete:
```bash
fd55 argo repo delete --repo-url https://github.com/davidpinhas/mc-server.git
```

Expected output:
```
2023-01-13 07:39:01,319|INFO|Deleted repository - https://github.com/davidpinhas/mc-server.git
```

## App
### Get Applications
Get all ArgoCD applications:
```bash
fd55 argo app list
```

Expected output:
```
2022-12-29 04:21:49,356|INFO|Getting ArgoCD applications

+-------------------------+
|       Application       |
+-------------------------+
|         my_app1         |
|         my_app2         |
+-------------------------+
```

### Create Application
Swagger ref - https://argo.mydomain.com/swagger-ui#operation/ApplicationService_Create

To create an application, use the `-f` option to provide the json file application spec:
```bash
fd55 argo app create --file create-app.json
```

Expected output:
```
2022-12-29 04:19:36,131|INFO|Successfully created application my_app
```

### Update Application
Swagger ref - https://argo.mydomain.com/swagger-ui#operation/ApplicationService_Update

To update an application:
```bash
fd55 argo app update --file create-app.json
```

Expected output:
```
2022-12-29 04:44:05,954|INFO|Successfully updated application my_app
```

### Delete Application
To delete an application, use the `-n` option to provide the name of the application you wish to delete:
```bash
fd55 argo app delete --name my_app
```

Expected output:
```
2022-12-29 04:44:28,556|INFO|Successfully deleted application
```

## Server
:warning: Limitation: The `server` command requires a local Kubectl client to be pre-configured with the desired Kubernetes cluster and the ArgoCD service must be running under the "argocd" namespace. Additionally, the pod name of the ArgoCD server must start with "**argocd-server**-xxxxx".

### Export ArgoCD server settings
To export the ArgoCD server settings, run the following command:
```bash
fd55 argo server export
```
This command will output the full settings of the ArgoCD server, which is required for the `import` command later.

To save the export output to a file, use the following command:
```bash
fd55 argo server export > argocd-export-$(date +%d-%m-%Y).yaml
```
This command will create a file with the full server settings, and will use the current date in the file name.

### Import ArgoCD server settings
To import the exported ArgoCD settings, run the command:
```bash
fd55 argo server import -f argocd-export-16-01-2023.yaml
```
The CLI will copy the file to the `/tmp` directory of the ArgoCD server pod and start the import.

### Create ArgoCD JWT token
To generate a JWT token, use the following command and provide the ArgoCD admin `user` and `password`:
```bash
fd55 argo server create-jwt -u $USER -p $PASSWORD
```

The output will print the newly generated JWT token:
```bash
2023-03-16 13:20:39,460|INFO|Generating JWT token
2023-03-16 13:20:40,348|INFO|Created JWT Token: eyJhb....
```

## OCI
---
[OCI (Oracle Cloud Infrastructure)](https://www.oracle.com/il-en/cloud/) integration utilizes the [KMS feature](https://www.oracle.com/il-en/security/cloud-security/key-management/) and lets you encrypt and decrypt a string.

### Commands
- [Vault](#Vault)
- [KMS](#KMS)
- [Load Balancer](#load-balancer)
- [WAF](#WAF)

This integration requires the following keys:
* `user` - The OCID of the user for whom the key pair is being added
* `fingerprint` - The fingerprint of the key that was just added.
* `tenancy` - Your tenancy's OCID.
* `region` - The currently selected region in the Console.
* `key_file` - The path to your downloaded private key file. You must update this value to the path on your file system where you saved the private key file.

For more details on retrieving the required keys, read more in Oracle's [minimum required keys and OCIDs](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#Required_Keys_and_OCIDs) Docs.
#TODO: Add support for encryption and decryption of binaries.

## Vault
### List vaults
To get a list of all current vaults under the tenancy that was set in the [Freedom 55 config file](#Configuration), run the following command:
```bash
fd55 oci vault list
```

The resulting output should be a table that lists all vaults:
```bash
2023-01-04 03:10:53,303|INFO|Retrieving vaults data
+----------------------+---------+----------------------------------+
|         Name         |  State  |           Time Created           |
+----------------------+---------+----------------------------------+
|      test-vault      | DELETED | 2022-10-31T18:14:22.516000+00:00 |
|      main-vault      |  ACTIVE | 2022-10-17T17:08:29.486000+00:00 |
+----------------------+---------+----------------------------------+
```

To print the ID of the vaults, you can add the `--id` argument:
```bash
fd55 oci vault list --id
```

### Set vault
In order to setup a vault with the CLI to perform the KMS operations, you can use:
```bash
fd55 oci vault set
```

Which will open an interactive menu for selecting the vault instance:
```bash
▶ fd55 oci vault set
2023-01-10 03:15:24,175|INFO|Retrieving active vaults
? Press enter to choose a KMS vault:
❯ test-vault
❯ test-vault2
❯ test-vault3
```

After selecting the desired KMS vault, the name of the vault will be added to the config.ini file under the OCI section.

The `set-vault` command only iteriates over vaults with **ACTIVE** 'lifecycle_state', therefore, newly created vault will not appear in the menu until reaching that state.

### Create vault
To create a new vault, use the command below and provide the `-n`/`--name` argument to name the vault:
```bash
fd55 oci vault create --name test-vault
```
The vault will be created as "*DEFAULT*" vault type.

### Delete vault
To schedule a vault deletion, you can use the following command:
```bash
fd55 oci vault delete --id $VAULT_ID
```

The default time for deletion is set to **30** days from the time this command was triggered.

To overwrite the days for deletion, you can use the `-d`/`--days` argument (the minimum value can be 7 days):
```bash
fd55 oci vault delete --id $VAULT_ID --days 7
```

## KMS
### Encrypt String
To encrypt a secret:
```bash
fd55 oci kms encrypt --string "This is my secret"
```

Expected output:
```
2022-12-29 04:55:43,132|INFO|Encrypting string with KMS
2022-12-29 04:55:43,309|INFO|Encrypted string value - Qf7eN7k3cJBlAFpAtSVaPqM....
(KMS encrypted secret)
```

### Decrypt With KMS
For decrypting a secret, the KMS encrypted value needs to be provided as a string (decrpyting needs to be performed with the same key the value was encrypted to begin with):
```bash
fd55 oci kms decrypt --string "Qf7eN7k3cJBlAFpAtSVaPqM...."
```

Expected output:
```
2022-12-29 04:56:08,020|INFO|Decrypting string with KMS
2022-12-29 04:56:08,184|INFO|Decrypted string - This is my secret
```

<a id="load-balancer"></a>
## Load Balancer
### List load banancers
To list all load balancers from the configure `tenancy`, run:
```bash
fd55 oci lb list
```

Expected output:
```
+---------------+--------+---------------------------+-----------------+
|      Name     | State  |        Time Created       |    Public IP    |
+---------------+--------+---------------------------+-----------------+
| K3s public LB | ACTIVE | 2022-12-01T01:50:06+00:00 | 123.123.123.123 |
+---------------+--------+---------------------------+-----------------+
```

## WAF
### List network security groups
To list the network security groups, run:
```bash
fd55 oci waf list-nsg
```

Expected output:
```
2023-01-25 00:51:45,400|INFO|Listing load balancer network security groups for ID - None
+---------------------------+-----------+----------------------------------+
|           Name            |   State   |           Time Created           |
+---------------------------+-----------+----------------------------------+
|       Kubeapi public      | AVAILABLE | 2022-12-01T01:50:02.117000+00:00 |
|  Kubernetes public LB nsg | AVAILABLE | 2022-12-01T01:50:02.063000+00:00 |
|      Workers public LB    | AVAILABLE | 2022-12-01T01:50:02.045000+00:00 |
+---------------------------+-----------+----------------------------------+
```

### List load banancer network security groups rules
To retrieve a specific load balancer NSG rules, run the following command with the `--id` argument:
```bash
fd55 oci waf list-nsg-rules --id ocid1.networksecuritygroup.oc1......
```
The command will return a table for each rule.

### Update load banancer network security groups rules
In order to update a LB NSG rule, run the following command:
```bash
fd55 oci waf update-nsg-rule \
    --id ocid1.networksecuritygroup.oc1... \
    --rule-id $NSG_RULE_ID \
    --protocol 6 \
    --direction INGRESS \
    --description 'Allow HTTPS from all' \
    --source '123.123.123.123/32' \
    --source-type CIDR_BLOCK \
    --destination-type CIDR_BLOCK \
    --tcp-destination-min 443 \
    --tcp-destination-max 443
```
The command should return an JSON response upon a successful update.

## SOPS
---
The SOPS integration encrypts and decrypts files using [Age encryption](https://github.com/FiloSottile/age).
Both encrypt and decrypt operations require an `-i`/`--input-file` and `-o`/`--output-file` file arguments. <br>**Limitation**: As the [SOPS SDK](https://github.com/mozilla/sops#12development-branch) only has support for Golang, the SOPS client is required to be installed, you can read more in the [Requirements section](#requirements).

This integration requires the following key:
* `key_file` - The path to the Age key.

To generate a secure key with Age for use with the SOPS integration, you can run the following command:
```bash
mkdir ~/.sops
age-keygen -o ~/.sops/key.txt
```

The `key_file` parameter requires the full path of the key file location, for example `/Users/$USER/.sops/key.txt`.

To run the command using a specific Age key, you may utilize the `-k`/`--key-file` option to set the path of the key:
```bash
fd55 sops encrypt --input-file values.yaml --output-file encrypted-values.yaml --key-file key.txt
```

### Encrypt File
Encrypt a file using SOPS with the following command, by providing the `-i`/`--input-file` and `-o`/`--output-file` files:
```bash
fd55 sops encrypt --input-file values.yaml --output-file encrypted-values.yaml
```

Expected output:
```
2022-12-29 05:13:38,099|INFO|Encrypting file with SOPS
2022-12-29 05:13:38,113|INFO|Finished encrypting encrypted-values.yaml file
```

### Encrypt Using Regex
For encrypting specific values, you may use the ``--encrypted-regex`` or ``-r`` flags to set a regex condition to encrypt:
```bash
fd55 sops encrypt --input-file values.yaml --output-file encrypted-values.yaml --encrypted-regex "ingress$"
```

Expected output:
```
2022-12-29 05:15:42,549|INFO|Encrypting file with SOPS
2022-12-29 05:15:42,549|INFO|Using regex: ingress$
2022-12-29 05:15:42,564|INFO|Finished encrypting encrypted-values.yaml file
```

### Encrypt Multiple Values With Regex
To encrypt multiple values, use the ``|`` sign:
```bash
fd55 sops encrypt --input-file values.yaml --output-file encrypted-values.yaml --encrypted-regex "ingress|domain|spec"
```

Expected output:
```
2022-12-29 05:52:53,955|INFO|Encrypting file with SOPS
2022-12-29 05:52:53,955|INFO|Using regex: ingress|domain|spec
2022-12-29 05:52:54,012|INFO|Finished encrypting encrypted-values.yaml file
```

### Decrypt File
In order to decrypt a file, use the following:
```bash
fd55 sops decrypt --input-file encrypted-values.yaml --output-file decrypted-values.yaml
```

Expected output:
```
2022-12-29 05:10:09,797|INFO|Decrypting file with SOPS
2022-12-29 05:10:09,858|INFO|Finished decrypting decrypted-values.yaml file
```

## Terraform
---
To run the [Terraform](https://www.terraform.io) integration, you will need to provide the path of Terraform project with ``--path`` or ``-p`` flags.

### Get Output From Terraform Plan
For example, run the command below to get the output of the Terraform plan:
```bash
fd55 tf output --path /path/to/tf/plan
```

### Initialize Terraform Plan
```bash
fd55 tf init --path /path/to/tf/plan
```

### Plan The Terraform Plan
```bash
fd55 tf plan --path /path/to/tf/plan
```

### Apply Terraform Plan
```bash
fd55 tf apply --path /path/to/tf/plan
```

### Destroy Terraform Plan
```bash
fd55 tf destroy --path /path/to/tf/plan
```

## Cloudflare
---
The [Cloudflare](https://www.cloudflare.com/en-gb/) integration utilizes the official [Cloudflare API](https://developers.cloudflare.com/api/) to perform its actions in the background to modify the configured domain DNS records.

### Commands
- [DNS](#CF-DNS)
- [WAF](#CF-WAF)

This integration requires the following keys:
* `email` - Email address used to authenticate with Cloudflare.
* `api_key` - API key with Read permissions for DNS Zone.
* `domain_name` - Domain name.

## CF-DNS
### List DNS records
In order to list all DNS records, run the following command:
```bash
fd55 cf dns list
```

Expected output:
```
2023-01-08 00:49:15,483|INFO|Retrieving DNS records for domain 'domain.com'
+----------------------------+-------+-------------------------+------+---------+
|            Name            |  Type |         Content         | TTL  | Proxied |
+----------------------------+-------+-------------------------+------+---------+
|         domain.com         |   A   |     123.123.123.123     |  60  |  False  |
|      blog.domain.com       | CNAME |      domain.com         |  1   |   True  |
+----------------------------+-------+-------------------------+------+---------+
```

To list the IDs of the DNS records, use the `--id` flag.

### DNS Records
Freedom 55 allows the user to modify domain DNS records by creating, updating and deleting records.

The **Create** and **Update** commands require the following arguments:
Option | Alias | Default| Description | Example | Required
--- | --- | --- | --- | --- | ---
`--name` | `-n` | NA | DNS name | "*sub.domain.com*" | **Yes**
`--content` | `-c` | NA | Target address content, can set IP or domain name | "*127.0.0.1*" | **Yes**
`--type` | `-t` | A | DNS record type | "*CNAME*" | **Yes**
`--ttl` | NA | 60 | Time to live | "*300*" | **No**
`--comment` | NA | "`DNS record updated with Freedom 55`" | Add comment to DNS record | "*New CNAME*" | **No**
`--proxied` | `-p` | `False` | Flag: Set proxy to TRUE | NA | **No**

### Create DNS record
To create a DNS record, we can run the following command:
```bash
fd55 cf dns create --name test.domain.com --content 123.123.123.123 --type A
```

The DNS will be created with the provided arguments and set default ones for the arguments that weren't provided, as we can see in the output:
```
2023-01-08 00:53:39,254|INFO|Creating DNS record 'test.domain.com'
2023-01-08 00:53:41,422|INFO|New metadata for 'test.domain.com' record:
2023-01-08 00:53:41,422|INFO| * id: $ID
2023-01-08 00:53:41,422|INFO| * zone_id: $ZONE_ID
2023-01-08 00:53:41,422|INFO| * zone_name: domain.com
2023-01-08 00:53:41,423|INFO| * name: test.domain.com
2023-01-08 00:53:41,423|INFO| * type: A
2023-01-08 00:53:41,430|INFO| * content: 123.123.123.123
2023-01-08 00:53:41,431|INFO| * proxiable: True
2023-01-08 00:53:41,431|INFO| * proxied: False
2023-01-08 00:53:41,431|INFO| * ttl: 60
2023-01-08 00:53:41,431|INFO| * locked: False
2023-01-08 00:53:41,431|INFO| * meta: {'auto_added': False, 'managed_by_apps': False, 'managed_by_argo_tunnel': False, 'source': 'primary'}
2023-01-08 00:53:41,431|INFO| * comment: DNS record updated with Freedom 55
2023-01-08 00:53:41,431|INFO| * tags: []
2023-01-08 00:53:41,431|INFO| * created_on: 2023-01-07T22:53:41.319273Z
2023-01-08 00:53:41,431|INFO| * modified_on: 2023-01-07T22:53:41.319273Z
2023-01-08 00:53:41,431|INFO|Finished modifying DNS record
```

The output will be similar to the update command.

### Update DNS record
In order to update the DNS record, use the following command:
```bash
fd55 cf dns update --name test.domain.com --content @ --type CNAME --proxied
```

In the above output we used the `@` sign to set the root address (the domain name) and configured the DNS record to be a *CNAME*.

### Delete DNS record
To delete a DNS record, you can use the below command and specify the full DNS name:
```bash
fd55 cf dns delete --name test.domain.com
```

Expected output:
```
2023-01-08 01:28:54,257|INFO|Deleting DNS record 'test.domain.com'
2023-01-08 01:28:55,169|INFO|Retrieving DNS record ID for test.domain.com
2023-01-08 01:28:58,198|INFO|Finished deleting DNS record 'test.domain.com'
```

## CF-WAF
### List firewall rules
To list firewall rules, run the following command:
```bash
fd55 cf waf list
```

Expected output:
```
2023-03-02 02:29:38,850|INFO|Retrieving firewall rules for domain 'domain.com'
+----------------------------------+-------------+--------------------------------------------------------------------------------------+
|                ID                | Description |                                      Expression                                      |
+----------------------------------+-------------+--------------------------------------------------------------------------------------+
|                id1               |  Whitelist  | (ip.src eq 123.123.123.123 and ip.src eq 124.124.124.124)                            |
|                id2               |  Blacklist  |  (ip.src in {0.0.0.0/0} and ip.src ne 123.123.123.123 and ip.src ne 124.124.124.124) |
+----------------------------------+-------------+--------------------------------------------------------------------------------------+
```

### Create firewall rule
To Create a firewall rule, you can run the following command:
```bash
fd55 cf waf create -a block -e "ip.src eq 123.123.123.123" --description "testing rule creation" -n test-rule
```
The command will create a firewall rule and a coresponding filter for the rule.

To view the full command options, run:
```bash
fd55 cf waf create --help
```

### Update firewall rule
For updating a firewall rule, you need to provide the firewall rule ID and the new expression:
```bash
fd55 cf waf update --id f5ed... -e "ip.src eq 12.12.12.12"
```
The ID of the firewall rule can be found by listing the run using `waf list` command.

### Delete firewall rule
To delete a firewall rule, provide the firewall rule ID or the name of the firewall rule when using the `waf delete` command.
The command will prompt a warning that the operation will delete the firewall rule and it's cooresponding firewall rule filter, with a request to approve the action:
```bash
fd55 cf waf delete --name test-rule
2023-03-15 19:03:34,246|WARNING|Deleting firewall rule and filter
Would you like to proceed? Y/n: Y
2023-03-15 19:03:39,051|INFO|Deleted firewall rule with ID f5ed...
```

### List firewall rule filters
Listing the firewall rules filters can be achieved with the following command:

```bash
fd55 cf waf list-filters
```

### Delete firewall rule filter
In case deleting a specific firewall rule filter is required, this is possible with the `waf delete-filter` command along with the rule filter ID:
```bash
fd55 cf waf delete-filter --id f5ed...
```

## ChatGPT
---
The [OpenAI](https://openai.com) integration utilizes the official [OpenAI API](https://beta.openai.com/docs/api-reference/introduction?lang=python) to access their language model engine, which is set to use the "*text-davinci-003*" engine by default.

This integration requires the following keys:
* `api_key` - OpenAI API key.

The OpenAI integration will use up your tokens according to your account plan.
Read here for more details on OpenAI [Rate Limits](https://beta.openai.com/docs/guides/rate-limits/what-are-the-rate-limits-for-our-api).  

## Chat
![](images/openai_chat.gif)

To send a message to model, run:
```bash
fd55 ai chat -p "create a bash script to backup and upgrade a kubernetes cluster"
```
The output should be printed to the console in chunks (EngineAPIResource generator events) as soon as they become available.

It is possible to pass a file with `--file` as a reference to your prompt. For example, we have the file test.py that we want to add logging to, to do so we can run:
```bash
fd55 ai chat -p "add logging" --file test.py
```
The test.py file content will be added to the passed prompt to add it as a reference.

In case you want to save the output to a new file, you can use the `--output` flag to print the full output:
```bash
fd55 ai chat -p "add logging" --file test.py --output > test2.py
```
The `--output` flag will wait for the full output to be retrieved and prints out the file content to the console.

### :warning: :books: Experimental Features of OpenAI Integration
This section provides an overview of the experimental features available with the OpenAI integration.

### -i/--iterations Flag
The `-i` or `--iterations` flag allows you to specify the number of iterations to use the same prompt over the same file.  
It is important to note that when using this flag, the `-f` or `--file` flag must also be passed in order for the iteration process to function correctly.  
:warning: Warning! This command will modify the specified file, therefore, it is highly recommended to manually backup the file before running the command.
By default, the command will create  a `$FILE_NAME.bak` file at the same directory with the original file content.

## Example
As an example, consider the following simple Python script, which sends a ping to Google:
```python
import os
hostname = "google.com"
response = os.system("ping -c 1 " + hostname)
if response == 0:
  print(hostname, 'is up!')
else:
  print(hostname, 'is down!')
```

By utilizing the `-i`/`--iterations` flag, you can specify the number of times this script should be executed with a specific prompt.  

For example, to improve specific sections of the file, you could use the command:
```bash
fd55 ai chat -p "improve code, add functionality, create threads, better performance" --file test.py --iterations 10
```

As shown in the following figure, you can see the results of the iteration process, where the script's performance and functionality were improved with each iteration:
![](images/openai_iterations_example.gif)

It is important to keep in mind that the larger the script, the longer each iteration will take and the token consumption will increase with each iteration.  
The current token limit is set to `2048`.

## Contribution
- Give a star. :star:
- Feel free to Fork and Clone. :beers:
- Check my [issues](https://github.com/davidpinhas/freedom55/issues) or create a [new issue](https://github.com/davidpinhas/freedom55/issues/new) and give me a PR with your bugfix or improvement after. I appreciate any help! ❤️
- Big thanks to the devs and contributors mentioned in the [CREDITS](/CREDITS.md) list.

## License
This project is licensed under the MIT License. See [LICENSE](/LICENSE.md) for more details.

