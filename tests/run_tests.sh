#!/bin/bash
echo "
#############################
##### Running CLI Tests #####
#############################"
TEST_RESULTS=true

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
if command -v age >/dev/null 2>&1 ; then
  age-keygen -o key.txt >/dev/null 2>&1
  python -m unittest tests/test_sops.py || TEST_RESULTS=false
  rm test-values.yaml enc-values.yaml key.txt 
else
  echo "WARN: Age command not found, install Age https://github.com/FiloSottile/age#installation"
  TEST_RESULTS=false
fi
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
export TEST_RESULTS
echo "
##########################
##### Finished Tests #####
##########################"
