from setuptools import setup
with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()


setup(
    name="fd55",
    version="3.9.3",
    description="Freedom 55 CLI is a operational tool to maintain a personal homelab",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Dave Pinhas",
    author_email="davepinhas89@gmail.com",
    url="https://github.com/davidpinhas/freedom55.git",
    classifiers=["Programming Language :: Python :: 3.10"],
    packages=[
        "fd55/cli/cli_groups",
        "fd55/cli/cli_groups/cli_options",
        "fd55/cli/cli_groups/cli_options/oci",
        "fd55/cli/cli_groups/cli_options/argocd",
        "fd55/cli/cli_groups/cli_options/cli_config",
        "fd55/cli/cli_groups/cli_options/cloudflare",
        "fd55/cli/chatgpt_client",
        "fd55/cli/oci_client",
        "fd55/cli/argocd_client",
        "fd55/cli/sops_client",
        "fd55/cli/tf_client",
        "fd55/cli/cloudflare_client",
        "fd55/cli",
        "fd55/utils",
        "fd55",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": ["fd55 = fd55.cli.fd55:main"]},
    install_requires=[
        "click",
        "oci",
        "retry",
        "requests",
        "InquirerPy",
        "prettytable",
        "kubernetes",
        "cloudflare",
        "tabulate",
        "openai",
        "colorlog"],
)
