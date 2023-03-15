#!/bin/bash
# Deactivate existing virtual env
deactivate &> /dev/null
echo "
############################
##### Freedom 55 Setup #####
############################
"
# Check OS
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Unix;;
    Darwin*)    machine=Unix;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

echo "INFO: Checking prequisites"
# Check Python 3 installed
if ! command -v python3 > /dev/null; then
  echo "ERROR: Python 3 is not installed on this system"
  echo "
You can install Python 3 using the following commands:
  * Debian/Ubuntu: sudo apt-get install python3 python3-pip python3-virtualenv
  * CentOS/RedHat: sudo yum install python3 python3-pip python3-virtualenv
  * Fedora: sudo dnf install python3 python3-pip python3-virtualenv
  * macOS: brew install python3 virtualenv
  * Windows:

Download the Python 3 installer from the official Python website: https://www.python.org/downloads/windows/
Run the installer and follow the prompts to install Python 3.
"
  return 0

# Check Python 3 version
echo "INFO: Checking Python 3 version"
fi
if [[ "${machine}" == "MinGw" ]]; then
  minor_version=$(python -c 'import sys; print(sys.version_info)' | awk '{print $2}' | grep -o '[0-9]\+')
else
  minor_version=$(python3 -c 'import sys; print(sys.version_info)' | awk '{print $2}' | grep -o '[0-9]\+')
fi
if [[ $minor_version -ge 10 ]]; then
  echo "INFO: Valid Python version"
else
  echo "ERROR: Python3 version is lower than 3.10, please install Python3.10 or above before proceeding."
  echo "INFO: For more details go to - https://www.python.org/downloads."
  return 0
fi

# Check pip3 installed
if ! command -v pip3 &> /dev/null; then
  echo "ERROR: PIP 3 is not installed"
  echo "You can install Python 3 using the following commands:
  * Debian/Ubuntu: sudo apt-get install python3-pip 
  * CentOS/RedHat: sudo yum install python3-pip
  * Fedora: sudo dnf install python3-pip
  * macOS: brew install python3
  * Windows:

Download the Python 3 installer from the official Python website: https://www.python.org/downloads/windows/
Run the installer and follow the prompts to install Python 3.
" 
  return 0
fi

# Check virtualenv installed
if [[ "${machine}" == "MinGw" ]]; then
  echo "INFO: Running on Windows, virtualenv not required"
elif ! command -v virtualenv &> /dev/null; then
  echo "ERROR: Virtualenv not installed"
  return 0
fi

# Set variables
if [[ "${machine}" == "MinGw" ]]; then
  python_bin="python"
  venv="python -m virtualenv freedom55-venv > /dev/null"
  venv_activate="source $PWD/freedom55-venv/Scripts/activate"
  pip install virtualenv &> /dev/null
else
  python_bin="python3"
  venv="virtualenv --python=python3 freedom55-venv"
  venv_activate="source $PWD/freedom55-venv/bin/activate"
fi

# Setting up source code virtual environment
if [ -d "freedom55-venv" ]; then
  # Virtualenv exists
  echo "INFO: Activating virtualenv"
  eval $venv_activate || { echo "ERROR: Failed to activate virtualenv."; return 0; }
  echo "INFO: Installing requirements"
  pip install -r requirements.txt &> /dev/null || { echo "ERROR: Failed to install requirements."; return 0; }
  echo "INFO: Developing setup.py"
  $python_bin setup.py develop &> /dev/null || { echo "ERROR: Failed to develop setup.py."; return 0; }
else
  # Virtualenv created
  echo "INFO: Creating virtualenv"
  eval $venv &> /dev/null || { echo "ERROR: Failed to create virtualenv."; return 0; }
  echo "INFO: Activating virtualenv"
  eval $venv_activate || { echo "ERROR: Failed to activate virtualenv."; return 0; }
  echo "INFO: Installing requirements"
  pip install -r requirements.txt &> /dev/null || { echo "ERROR: Failed to install requirements."; return 0; }
  echo "INFO: Developing setup.py"
  $python_bin setup.py develop &> /dev/null || { echo "ERROR: Failed to develop setup.py."; return 0; }
  eval $venv_activate
fi

# Output message
echo "
################
##### Done #####
################
"
echo "INFO: Freedom 55 was initialized successfully."
echo "INFO: Run 'fd55' to test the CLI."

# Set up the alias command
alias_name=$(printf "alias fd55CLI='cd %s && source freedom55-venv/bin/activate'" "$PWD")
  
# Print the instructions to configure the CLI on the local machine with an alias
echo "
To configure the CLI on the local machine, run these three commands:"
echo "
### set alias to access the CLI directory and activate virtual environment"
printf '---
$ if ! grep -q "%s" ~/.bashrc; then echo "%s" >> %s' "$alias_name" "$alias_name" "~/.bashrc; fi
"
echo "
### Source bashrc file"
echo "---
$ source ~/.bashrc
"
echo "### Run alias"
echo "---
$ fd55CLI
"