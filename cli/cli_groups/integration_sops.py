import click


@click.group()
@click.pass_context
def sops(ctx):
    """ SOPS with Age encryption commands """
    ctx.ensure_object(dict)


@sops.command()
@click.option('-i', '--input_file', help='file to encrypt', required=True)
@click.option('-o',
              '--output_file',
              help='encrypted output file',
              required=True)
@click.option('-r',
              '--encrypted_regex',
              help='set the encrypted key suffix',
              required=False)
@click.option('-k', '--key_file', help='Age full key path', required=False)
@click.pass_context
def encrypt(ctx, input_file, output_file, encrypted_regex, key_file):
    """ Encrypt file using SOPS with Age encryption """
    from cli.sops_client.sops_cli import Sops
    Sops.encrypt(
        input_file=input_file,
        output_file=output_file,
        encrypted_regex=encrypted_regex, key_file=key_file)


@sops.command()
@click.option('-i', '--input_file', help='file to decrypt', required=True)
@click.option('-o',
              '--output_file',
              help='decrypted output file',
              required=True)
@click.option('-k', '--key_file', help='Age full key path', required=False)
@click.pass_context
def decrypt(ctx, input_file, output_file, key_file=None):
    """ Decrypt file using SOPS with Age encryption """
    from cli.sops_client.sops_cli import Sops
    Sops.decrypt(
        input_file=input_file,
        output_file=output_file,
        key_file=key_file)
