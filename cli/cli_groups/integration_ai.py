import click
from utils.cli_help_order import CliHelpOrder
from cli.chatgpt_client.chatgpt_cli import ChatGPT


@click.group(cls=CliHelpOrder)
@click.pass_context
def ai(ctx):
    """ OpenAI Commands """
    ctx.ensure_object(dict)


@ai.command(help_priority=1)
@click.option('-p', '--prompt', help='Prompt to send ChatGPT', required=True)
@click.option('-o',
              '--output',
              help='Returns the full output when fully generated',
              is_flag=True)
@click.option('-f',
              '--file',
              help='Set a file as reference in the prompt',
              required=False)
@click.option('-i',
              '--iterations',
              help='Number of iterations to use the propmt over a file',
              required=False)
@click.pass_context
def chat(ctx, prompt, output=None, file=None, iterations=None):
    """ ChatGPT chat """
    chat = ChatGPT()
    chat.send_openai_request(
        prompt=str(prompt),
        full_output=output,
        file=file,
        iterations=iterations)
