#!/bin/bash
deactivate &> /dev/null
echo "
############################
##### Freedom 55 Setup #####
############################
"
echo "INFO: Installing prequisites"
if ! command -v python3 > /dev/null; then
  # Python 3 is not installed
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
else
  if [ "$OSTYPE" == "win32" ] || [ "$OSTYPE" == "msys" ]; then  
    minor_version=$(python -c 'import sys; print(sys.version_info)' | awk '{print $2}' | grep -o '[0-9]\+')
  else
    minor_version=$(python3 -c 'import sys; print(sys.version_info)' | awk '{print $2}' | grep -o '[0-9]\+')
  fi
  if [[ $minor_version -ge 10 ]]; then
    echo "INFO: Valid Python version"
  else
    echo "ERROR: Python3 version is lower than 3.10, please install Python3.10 or above before proceeding."
    echo "INFO: For more details go to - https://www.python.org/downloads."
  fi
fi
# Check if pip3 is installed
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
# Check if virtualenv is installed
if [ "$OSTYPE" == "win32" ] || [ "$OSTYPE" == "msys" ]; then
  echo "INFO: Running on Windows, virtualenv not required"
elif ! command -v virtualenv &> /dev/null; then
  echo "ERROR: Virtualenv not installed"
  return 0
fi

if [ "$OSTYPE" == "win32" ] || [ "$OSTYPE" == "msys" ]; then
  python_bin="python"
  venv="python -m virtualenv freedom55-venv > /dev/null"
  venv_activate="source $PWD/freedom55-venv/Scripts/activate"
  pip install virtualenv &> /dev/null
else
  python_bin="python3"
  venv="virtualenv --python=python3 freedom55-venv"
  venv_activate="source $PWD/freedom55-venv/bin/activate"
fi
# Setting up source code
if [ -d "freedom55-venv" ]; then
  # Virtualenv exists
  echo "INFO: Activating virtualenv"
  $venv_activate
  echo "INFO: Installing requirements"
  pip install -r requirements.txt &> /dev/null
  echo "INFO: Developing setup.py"
  $python_bin setup.py develop
else
  # Virtualenv created
  echo "INFO: Creating virtualenv"
  eval $venv
  sleep 1
  echo "INFO: Activating virtualenv"
  eval $venv_activate
  echo "INFO: Installing requirements"
  pip install -r requirements.txt &> /dev/null
  echo "INFO: Developing setup.py"
  $python_bin setup.py develop &> /dev/null
fi

# Output message
echo "
################
##### Done #####
################
"
echo "INFO: Freedom 55 was initialized successfully."

# Set up the alias command
alias_name=$(printf "alias fd55CLI='cd %s && source freedom55-venv/bin/activate'" "$PWD")
  
# Print the instructions to configure the CLI on the local machine
echo "To configure the CLI on the local machine, run these three commands:"
echo "
# set alias to access the current directory and activate venv"
printf '$ if ! grep -q "%s" ~/.bashrc; then echo "%s" >> %s' "$alias_name" "$alias_name" "~/.bashrc; fi
"
echo "
# Source the bashrc file"
echo "$ source ~/.bashrc
"
echo "# Run the alias"
echo "$ fd55CLI
"