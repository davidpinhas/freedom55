if [ -d "/venv" ]; then
  # Virtualenv Exists
  source venv/bin/activate
  pip install -r requirements.txt
  python3.10 setup.py develop
  cd ../
else
  # Virtualenv created
  virtualenv --python=python3.10 venv
  sleep 1
  source venv/bin/activate
  pip install -r requirements.txt
  python3.10 setup.py develop
fi
