#!/bin/bash
echo "
#############################
##### Running CLI Tests #####
#############################"
TEST_RESULTS=true

# Check Age exists
if command -v age >/dev/null 2>&1 ; then
  age-keygen -o key.txt >/dev/null 2>&1
else
  echo "WARN: Age command not found, install Age https://github.com/FiloSottile/age#installation"
  TEST_RESULTS=false
fi

while [[ $# -gt 0 ]]
do
key="$1"
# Arguments
case $key in
    -u|--oci-user)
    OCI_USER="$2"
    shift
    ;;
    -f|--oci-fingerprint)
    OCI_FINGERPRINT="$2"
    shift
    ;;
    -t|--oci-tenancy)
    OCI_TENANCY="$2"
    shift
    ;;
    -r|--oci-region)
    OCI_REGION="$2"
    shift
    ;;
    -k|--oci-key-file)
    OCI_KEY_FILE="$2"
    shift
    ;;
    -v|--oci-vault)
    OCI_VAULT="$2"
    shift
    ;;
    -a|--argocd-url)
    ARGO_URL="$2"
    shift
    ;;
    -b|--argocd-token)
    ARGO_TOKEN="$2"
    shift
    ;;
    -e|--cloudflare-email)
    CLOUDFLARE_EMAIL="$2"
    shift
    ;;
    -c|--cloudflare-api-key)
    CLOUDFLARE_API_KEY="$2"
    shift
    ;;
    -d|--cloudflare-domain)
    CLOUDFLARE_DOMAIN="$2"
    shift
    ;;
    *)

    ;;
esac
shift
done

# Create the config directory if it doesn't exist
if [ ! -d "$HOME/.fd55" ]; then
    mkdir $HOME/.fd55
fi

# Make a backup of the existing config file
if [ -f ~/.fd55/config.ini ]; then
  echo "INFO: Backing up existing config file to backup-config.ini"
  cp ~/.fd55/config.ini ~/.fd55/backup-config.ini
fi

echo "
##### Running Config tests #####"
python -m unittest tests/test_config.py || TEST_RESULTS=false

# Check that at least one argument was provided
if [ -n "$OCI_USER" ] || [ -n "$OCI_FINGERPRINT" ] || [ -n "$OCI_TENANCY" ] || [ -n "$OCI_REGION" ] || [ -n "$OCI_KEY_FILE" ] || [ -n "$OCI_VAULT" ] ||  [ -n "$ARGO_URL" ] || [ -n "$ARGO_TOKEN" ] || [ -n "$CLOUDFLARE_EMAIL" ] || [ -n "$CLOUDFLARE_API_KEY" ] || [ -n "$CLOUDFLARE_DOMAIN" ]; then
# Create config file
  cat << EOF > ~/.fd55/config.ini
[OCI]
user = $OCI_USER
fingerprint = $OCI_FINGERPRINT
tenancy = $OCI_TENANCY
region = $OCI_REGION
key_file = $OCI_KEY_FILE
kms_vault = $OCI_VAULT

[SOPS]
key_file = key.txt

[ARGOCD]
url = $ARGO_URL
api_token = $ARGO_TOKEN

[CLOUDFLARE]
email = $CLOUDFLARE_EMAIL
api_key = $CLOUDFLARE_API_KEY
domain_name = $CLOUDFLARE_DOMAIN
EOF
else
    echo "INFO: Skipping config file creation, no arguments provided."
    cp ~/.fd55/backup-config.ini ~/.fd55/config.ini
fi

# TESTS
echo "
##### Running OCI tests #####"
python -m unittest tests/test_oci.py || TEST_RESULTS=false

echo "
##### Running Cloudflare tests #####"
python -m unittest tests/test_cf.py || TEST_RESULTS=false

echo "
##### Running Terraform tests #####"
cat << EOF > tmp_tf_test.tf
resource "null_resource" "example" {
  # Empty resource
}
EOF
python -m unittest tests/test_tf.py || TEST_RESULTS=false
rm tmp_tf_test.tf

echo "
##### Running SOPS tests #####"
cat << EOF > test-values.yaml
test:
    key1: value1
EOF
python -m unittest tests/test_sops.py || TEST_RESULTS=false

echo "
##### Running ArgoCD tests #####"
cat << EOF > tmp_argo_app.json
{
  "kind": "Application",
  "metadata": {
    "name": "freedom55-argo-test-app",
    "namespace": "argocd"
  },
  "spec": {
    "destination": {
      "namespace": "freedom55-argo-test-app",
      "server": "https://kubernetes.default.svc"
    },
    "project": "default",
    "source": {
      "path": "sync-waves",
      "repoURL": "https://github.com/argoproj/argocd-example-apps",
      "targetRevision": "HEAD"
    },
    "syncPolicy": {
      "automated": {
        "prune": true,
        "selfHeal": true
      },
      "syncOptions": [
        "CreateNamespace=true"
      ]
    }
  }
}
EOF
python -m unittest tests/test_argo.py || TEST_RESULTS=false
rm tmp_argo_app.json
if [[ "$TEST_RESULTS" = "true" ]] ; then
  echo "### INFO: All tests passed! ###"
else
  echo "### ERROR: Tests failed! ###"
fi

# Cleanup
rm test-values.yaml enc-values.yaml key.txt 
if [ -f ~/.fd55/backup-config.ini ]; then
  rm ~/.fd55/config.ini
  cp ~/.fd55/backup-config.ini ~/.fd55/config.ini
fi

export TEST_RESULTS
echo "
##########################
##### Finished Tests #####
##########################"
