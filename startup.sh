# Check the operating system
echo "
############################
##### Freedom 55 Setup #####
############################
"
if [ -d "venv" ]; then
  # Virtualenv Exists
  echo "INFO: Activating virtualenv..."
  source $PWD/venv/bin/activate
  echo "INFO: Installing requirements..."
  pip install -r requirements.txt &> /dev/null
  echo "INFO: Developing setup.py..."
  python3 setup.py develop &> /dev/null
else
  # Virtualenv created
  echo "INFO: Creating virtualenv..."
  python3 -m venv venv &> /dev/null
  sleep 1
  echo "INFO: Activating virtualenv..."
  source $PWD/venv/bin/activate
  echo "INFO: Installing requirements..."
  pip install -r requirements.txt &> /dev/null
  echo "INFO: Developing setup.py..."
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
alias_name=$(printf "alias fd55CLI='cd %s && source venv/bin/activate'" "$PWD")
  
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