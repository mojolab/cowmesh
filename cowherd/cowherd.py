import click

@click.command()
@click.option("--test_key_auth" help="what to do")
@click.option("--host", prompt="hostname to connect to")
@click.option("--user",default="root",prompt="User: <root>?")


