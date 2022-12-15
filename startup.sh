if [ -d "venv" ]; then
  # Virtualenv Exists
  source venv/bin/activate
  pip install -r requirements.txt
  python3.10 setup.py develop
else
  # Virtualenv created
  virtualenv --python=python3.10 venv
  sleep 1
  source venv/bin/activate
  pip install -r requirements.txt
  python3.10 setup.py develop
fi

current_dir=$PWD
alias_name=$(printf "alias argusCLI='cd %s/argus && source venv/bin/activate'" "$current_dir")

echo "Argus was initialized successfully.
To configure the CLI on the local machine, Run the following commands:
"
printf 'echo "%s" >> %s' "$alias_name" "~/.bashrc"
echo "
source ~/.bashrc
argusCLI"