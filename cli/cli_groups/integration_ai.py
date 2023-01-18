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
@click.pass_context
def chat(ctx, prompt):
    """ ChatGPT chat """
    chat = ChatGPT()
    chat.send_openai_request(prompt=str(prompt))
