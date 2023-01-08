#!/bin/bash
echo "
#############################
##### Running CLI tests #####
#############################"
echo "
##### Running OCI tests #####"
python -m unittest tests/test_oci.py
echo "
##### Running Cloudflare tests #####"
python -m unittest tests/test_cf.py

