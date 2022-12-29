#!/bin/bash

# Validate arguments
if [ "$#" -ne 3 ]; then
  echo "Error: script requires three arguments (username, password and repository-url)"
  echo "Usage: script.sh [username] [password] [repository-url]"
  echo "Example: $ script.sh admin Password1 https://demo.jfrog.io/artifactory/api/pypi/pypi"
  exit 1
fi

# Cleanup
rm -rf arg.spec fd55.spec freedom55-venv build dist ..spec fd55.egg-info

# Binary creation
python3 setup.py sdist bdist_wheel

# User arguments
username=$1
password=$2
repository_url=$3

# Run the twine upload 
twine upload --username $username --password $password --repository-url $repository_url dist/*
