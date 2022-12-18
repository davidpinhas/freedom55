from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="argus",
    version="1.0.0",
    description="Argus CLI is a operational tool to maintain a personal homelab",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Dave Pinhas",
    author_email="davepinhas89@gmail.com",
    url="ssh://git@github.com:davidpinhas/argus.git",
    classifiers=["Programming Language :: Python :: 3.10"],
    packages=[
        "cli/cli_groups",
        "cli/oci_client",
        "cli/argocd_client",
        "cli/sops_client",
        "cli/tf_client",
        "cli",
        "utils",
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["argus = cli.argus:main"]},
    install_requires=["click", "oci", "requests", "python_terraform"],
)
