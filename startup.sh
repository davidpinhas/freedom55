#!/bin/bash
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
  * macOS: brew install python3 python3-pip python3-virtualenv
  * Windows:

Download the Python 3 installer from the official Python website: https://www.python.org/downloads/windows/
Run the installer and follow the prompts to install Python 3.
"
  exit 0
else
  minor_version=$(python3 -c 'import sys; print(sys.version_info)' | awk '{print $2}' | grep -o '[0-9]\+')
  if [[ $minor_version -ge 10 ]]; then
    echo "INFO: Valid Python version"
  # Check the operating system
  else
    # Install Python 3.10
    # On Debian/Ubuntu systems
    if [ -x "$(command -v apt-get)" ]; then
      sudo apt-get update
      sudo apt-get install python3.10 python3-virtualenv python3-pip -y
    # On CentOS/RedHat systems
    elif [ -x "$(command -v yum)" ]; then
      sudo yum install python3.10 python3-virtualenv python3-pip -y
    # On Fedora systems
    elif [ -x "$(command -v dnf)" ]; then
      sudo dnf install python3.10 python3-virtualenv python3-pip -y
    # On macOS systems
    elif [ "$(uname)" == "Darwin" ]; then
      # Install Homebrew if it is not already installed
      if ! [ -x "$(command -v brew)" ]; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
      fi
      brew install python3.10 -y
    # On Windows systems
    elif [ "$(uname)" == "Windows" ]; then
      # Download the Python 3.10 installer
      curl -O https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
      # Run the installer
      .\python-3.10.0-amd64.exe
      # Clean up
      rm python-3.10.0-amd64.exe
    else
      echo "ERROR: Could not detect operating system. Please install Python 3.10 and virtualenv manually."
      exit 1
    fi
  fi
fi
# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
  echo "ERROR: PIP 3 is not installed"
  echo "You can install Python 3 using the following commands:
  * Debian/Ubuntu: sudo apt-get install python3-pip 
  * CentOS/RedHat: sudo yum install python3-pip
  * Fedora: sudo dnf install python3-pip
  * macOS: brew install python3-pip
  * Windows:

Download the Python 3 installer from the official Python website: https://www.python.org/downloads/windows/
Run the installer and follow the prompts to install Python 3.
" 
  return 0
fi
# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
  # Install virtualenv
  echo "INFO: Installing Virtualenv"
  pip3 install python3-virtualenv &> /dev/null
fi

# Setting up source code
if [ -d "freedom55-venv" ]; then
  # Virtualenv exists
  echo "INFO: Activating virtualenv"
  source $PWD/freedom55-venv/bin/activate
  echo "INFO: Installing requirements"
  pip install -r requirements.txt &> /dev/null
  echo "INFO: Developing setup.py"
  python3 setup.py develop &> /dev/null
else
  # Virtualenv created
  echo "INFO: Creating virtualenv"
  virtualenv --python=python3 freedom55-venv &> /dev/null
  sleep 5
  echo "INFO: Activating virtualenv"
  source $PWD/freedom55-venv/bin/activate
  echo "INFO: Installing requirements"
  pip install -r requirements.txt &> /dev/null
  echo "INFO: Developing setup.py"
  python3 setup.py develop &> /dev/null
fi

# Print the ASCII art and a message to the console
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