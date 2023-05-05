import click


@click.group()
@click.pass_context
def sops(ctx):
    """ SOPS with Age encryption commands """
    ctx.ensure_object(dict)


@sops.command()
@click.option('-i', '--input-file', help='file to encrypt', required=True)
@click.option('-o', '--output-file', help='encrypted output file')
@click.option('-r', '--encrypted-regex', help='set the encrypted key suffix')
@click.option('-k', '--key-file', help='Age full key path')
@click.option('--in-place', help='modify file inplace', is_flag=True)
@click.pass_context
def encrypt(ctx, input_file, output_file, encrypted_regex, key_file, in_place):
    """ Encrypt file using SOPS with Age encryption """
    from fd55.cli.sops_client.sops_cli import Sops
    if in_place and output_file:
        raise click.UsageError(
            "Cannot specify both --in-place and --output-file")
    if in_place:
        output_file = input_file
    Sops.encrypt(
        input_file=input_file,
        output_file=output_file,
        encrypted_regex=encrypted_regex,
        key_file=key_file,
        in_place=in_place)


@sops.command()
@click.option('-i', '--input-file', help='file to decrypt', required=True)
@click.option('-o', '--output-file', help='decrypted output file')
@click.option('--in-place', help='modify file inplace', is_flag=True)
@click.option('-k', '--key-file', help='Age full key path')
@click.pass_context
def decrypt(ctx, input_file, output_file, in_place, key_file=None):
    """ Decrypt file using SOPS with Age encryption """
    from fd55.cli.sops_client.sops_cli import Sops
    if in_place and output_file:
        raise click.UsageError(
            "Cannot specify both --in-place and --output-file")
    if in_place and output_file is None:
        output_file = input_file
    Sops.decrypt(
        input_file=input_file,
        output_file=output_file,
        key_file=key_file,
        in_place=in_place)
