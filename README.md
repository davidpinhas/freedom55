# Argus
Argus CLI is an operational tool written in Python by David Pinhas to maintain, modify and operate a homelab.

```bash
$ argus
Usage: argus [OPTIONS] COMMAND [ARGS]...

  Argus CLI tools.

  The Argus CLI is an operational tool crafted by David Pinhas To maintain,
  modify and operate a homelab.

Options:
  --log TEXT  Logging level (INFO, WARNING, ERROR, CRITICAL, DEBUG)
  --help      Show this message and exit.

Commands:
  oci  OCI commands
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
git clone https://github.com/davidpinhas/argus.git
cd argus
bash startup.sh
```
The script will create a virtual environment and provide steps to configure the alias for sourcing the venv.

## Usage
To use the Argus CLI, we'll first call Argus, that the component and it's sub-command:
```bash
$ argus [COMPONENT] [COMMAND] [OPTIONS]
```
For example:
```bash
$ argus oci encrypt --string "Random text"
```

### Options
- `--string`: (Mandatory) Provide a string to encrypt/decrypt using OCI KMS.
- `--log DEBUG`: (Optional) Specify the log level. If not provided, the default level is INFO.
- `--help`: (Optional) Show the help message and exit.

### Examples
##### Encrypting a string:
To encrypt a secret, you can provide it as a string:
```bash
$ argus oci encrypt --string "This is my secret"
```

Expected output:
```
INFO:root:Validating OCI config file
INFO:root:All config keys exist
INFO:root:Encrypting string with KMS
INFO:root:Encrypted string value - Qf7eN7k3cJBlAFpAtSVaPqM.... (KMS encrypted secret)
```

##### Decrypting a secret:
For decrypting a secret, the KMS encrypted value needs to be provided as a string (decrpyting needs to be performed with the same key the value was encrypted to begin with):
```bash
$ argus oci decrypt --string Qf7eN7k3cJBlAFpAtSVaPqM....
```

Expected output:
```
INFO:root:Validating OCI config file
INFO:root:All config keys exist
INFO:root:Decrypting string with KMS
INFO:root:Decrypted string - This is my secret
```

## License
This project is licensed under the MIT License. See [LICENSE](/LICENSE.md) for more details.
