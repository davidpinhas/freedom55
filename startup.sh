# Check the operating system
if [ "$(uname)" == "Darwin" ]; then
  # MacOS
  if command -v figlet > /dev/null; then
    brew install figlet
  else
    echo "Info: Figlet already installed"
  fi
elif [ "$(uname)" == "Linux" ]; then
  # Linux
  if command -v apt-get > /dev/null; then
    # Debian-based systems (e.g. Ubuntu, Linux Mint)
    apt-get update
    apt-get install figlet
  elif command -v yum > /dev/null; then
    # Red Hat-based systems (e.g. CentOS, Fedora)
    yum install figlet
  elif command -v pacman > /dev/null; then
    # Arch-based systems (e.g. Manjaro)
    pacman -S figlet
  else
    echo "Error: unsupported Linux distribution"
    exit 1
  fi
elif [ "$(uname)" == "FreeBSD" ]; then
  # FreeBSD
  pkg install figlet
elif [ "$(uname)" == "MINGW64_NT-10.0" ] || [ "$(uname)" == "MINGW32_NT-10.0" ]; then
  # Windows (using Chocolatey)
  choco install figlet
else
  echo "Error: unsupported operating system"
  exit 1
fi

echo "figlet installed successfully"

figlet -f epic "Freedom 55"

if [ -d "venv" ]; then
  # Virtualenv Exists
  source venv/bin/activate
  pip install -r requirements.txt
  python3 setup.py develop
else
  # Virtualenv created
  virtualenv --python=python3 venv
  sleep 1
  source venv/bin/activate
  pip install -r requirements.txt
  python3 setup.py develop
fi

current_dir=$PWD
alias_name=$(printf "alias fd55CLI='cd %s/fd55 && source venv/bin/activate'" "$current_dir")

echo "Freedom 55 was initialized successfully.
To configure the CLI on the local machine, Run the following commands:
"
printf 'echo "%s" >> %s' "$alias_name" "~/.bashrc"
echo "
source ~/.bashrc
fd55CLI"